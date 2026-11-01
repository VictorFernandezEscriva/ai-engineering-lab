"use strict";
// All dynamic text goes through textContent (via h), never innerHTML.
const STATUS_LABEL = { pending: "Pending", studying: "Studying", practiced: "Practiced", validated: "Validated" };
const KINDS = ["exercise", "test", "evaluation", "comment", "file"];
let catalog, state, nodeById, exerciseById;

function h(tag, attrs, ...children) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else if (v !== false && v != null) el.setAttribute(k, v);
  }
  for (const c of children.flat()) if (c != null) el.append(c);
  return el;
}

async function api(path, body) {
  const opts = body === undefined ? {} : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  const res = await fetch(path, opts);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || res.statusText);
  return data;
}

const statusOf = (id) => state.status[id] || "pending";
const badge = (s) => h("span", { class: "badge " + s }, STATUS_LABEL[s] || s);
const nodeLink = (id) => h("a", { href: "#/node/" + id }, nodeById[id] ? nodeById[id].name : id);
const fmt = (iso) => (iso ? new Date(iso).toLocaleString() : "—");

async function load() {
  [catalog, state] = await Promise.all([api("/api/catalog"), api("/api/state")]);
  nodeById = Object.fromEntries(catalog.nodes.map((n) => [n.id, n]));
  exerciseById = Object.fromEntries(catalog.exercises.map((e) => [e.id, e]));
}

function formWith(fields, submitLabel, onSubmit) {
  const form = h("form", {}, fields, h("button", { type: "submit" }, submitLabel));
  const err = h("span", { class: "error" });
  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    err.textContent = "";
    try { await onSubmit(new FormData(form)); await render(); }
    catch (e) { err.textContent = e.message; }
  });
  form.append(err);
  return form;
}

function nodeSelect(name, selected) {
  return h("select", { name }, h("option", { value: "" }, "— none —"),
    catalog.nodes.map((n) => h("option", { value: n.id, selected: n.id === selected }, n.name)));
}

function dashboard() {
  const counts = { pending: 0, studying: 0, practiced: 0, validated: 0 };
  catalog.nodes.forEach((n) => counts[statusOf(n.id)]++);
  const plan = state.plan;
  const root = h("div", {},
    h("div", { class: "card" }, h("strong", {}, "Professional goal"), h("p", {}, catalog.goal)),
    h("h2", {}, "Current learning target"),
    h("div", { class: "card" },
      plan.next_node_id || plan.next_text
        ? [plan.next_node_id ? h("p", {}, "Topic: ", nodeLink(plan.next_node_id)) : null,
           plan.next_text ? h("p", {}, plan.next_text) : null]
        : h("p", { class: "muted" }, "Nothing stored; the map shows " + nodeById[catalog.default_target].name + " (default from ROADMAP.md). The note below is operational and does not replace ROADMAP.md."),
      formWith([nodeSelect("next_node_id", plan.next_node_id),
                h("input", { type: "text", name: "next_text", placeholder: "Next lesson / exercise", value: plan.next_text })],
        "Save target", (f) => api("/api/plan", { next_node_id: f.get("next_node_id"), next_text: f.get("next_text") }))),
    h("h2", {}, "Progress (self-reported)"),
    h("div", { class: "card" },
      Object.entries(counts).map(([s, n]) => h("span", {}, badge(s), " ", String(n), " ")),
      h("p", { class: "muted" }, `${catalog.nodes.length} knowledge nodes. Status is set by you; passing tests is not mastery. Last activity: ${fmt(state.last_activity)}`)),
    h("h2", {}, "Areas"),
    h("div", { class: "grid" }, catalog.areas.map((a) => {
      const ns = catalog.nodes.filter((n) => n.area === a.id);
      const exs = catalog.exercises.filter((e) => e.area === a.id).length;
      return h("div", { class: "card" }, h("strong", {}, a.name), h("p", { class: "muted" }, a.description),
        h("p", {}, `${ns.length} nodes · ${exs} exercises · ${ns.filter((n) => statusOf(n.id) === "validated").length} validated`));
    })),
    h("h2", {}, "Pending tasks"),
    h("div", { class: "card" },
      h("ul", { class: "plain" }, state.tasks.map((t) => h("li", {},
        h("label", {}, h("input", { type: "checkbox", checked: t.done ? "" : false,
          onchange: async (ev) => { await api("/api/tasks/" + t.id, { done: ev.target.checked }); await render(); } }),
          " ", t.done ? h("s", {}, t.text) : t.text)))),
      formWith([h("input", { type: "text", name: "text", placeholder: "New task" })], "Add task",
        (f) => api("/api/tasks", { text: f.get("text") }))),
    h("h2", {}, "Recent sessions"),
    h("div", { class: "card" },
      state.sessions.length ? h("ul", { class: "plain" }, state.sessions.map((s) => h("li", {},
        fmt(s.created_at), " — ", s.node_id ? [nodeLink(s.node_id), ": "] : null, s.note)))
        : h("p", { class: "muted" }, "No sessions logged."),
      formWith([nodeSelect("node_id", ""), h("input", { type: "text", name: "note", placeholder: "What did you do?" })],
        "Log session", (f) => api("/api/sessions", { node_id: f.get("node_id"), note: f.get("note") }))));
  return root;
}

const SVG_NS = "http://www.w3.org/2000/svg";
function sv(tag, attrs, ...children) {
  const el = document.createElementNS(SVG_NS, tag);
  for (const [k, v] of Object.entries(attrs || {})) if (v != null && v !== false) el.setAttribute(k, v);
  for (const c of children.flat()) if (c != null) el.append(c);
  return el;
}

const NW = 152, NH = 40, GAP = 8, ROW = 52, TOP = 50, PAD = 10;
const GLYPH = { pending: "○", studying: "◔", practiced: "◑", validated: "✓" };

// Lane layout, computed from the catalog. Columns = areas (route order). Inside a lane, rows follow the
// lane's own prerequisite chain. Each lane is then shifted down only as far as needed so that its
// cross-lane prerequisites sit above it; so a later phase starts right after what it depends on,
// not at a depth inflated by unrelated chains.
function layout() {
  const nodes = catalog.nodes;
  const local = {};
  const localDepth = (id) => local[id] ?? (local[id] = Math.max(-1, ...nodeById[id].prerequisites
    .filter((p) => nodeById[p].area === nodeById[id].area).map(localDepth)) + 1);
  nodes.forEach((n) => localDepth(n.id));
  const row = {};
  const shift = {};
  const placed = (id) => row[id] ?? (row[id] = local[id] + laneShift(nodeById[id].area));
  const laneShift = (area) => {
    if (shift[area] !== undefined) return shift[area];
    shift[area] = 0; // guards against cyclic lane dependencies (validated away in the catalog)
    let s = 0;
    for (const n of nodes) {
      if (n.area !== area) continue;
      for (const p of n.prerequisites) {
        if (nodeById[p].area !== area) s = Math.max(s, placed(p) + 1 - local[n.id]);
      }
    }
    return (shift[area] = s);
  };
  catalog.areas.forEach((a) => laneShift(a.id));
  nodes.forEach((n) => placed(n.id));
  const groups = {};
  nodes.forEach((n) => { const k = n.area + "|" + row[n.id]; (groups[k] = groups[k] || []).push(n.id); });
  const colX = {}, colW = {};
  let x = PAD;
  for (const a of catalog.areas) {
    const widest = Math.max(1, ...Object.entries(groups).filter(([k]) => k.startsWith(a.id + "|")).map(([, g]) => g.length));
    colW[a.id] = widest * (NW + GAP) + GAP;
    colX[a.id] = x;
    x += colW[a.id] + 8;
  }
  const pos = {};
  for (const [k, ids] of Object.entries(groups)) {
    const [area, r] = k.split("|");
    ids.forEach((id, i) => (pos[id] = { x: colX[area] + GAP + i * (NW + GAP), y: TOP + Number(r) * ROW }));
  }
  const maxY = Math.max(...Object.values(pos).map((p) => p.y)) + NH + PAD;
  return { pos, colX, colW, width: x + PAD, height: maxY };
}

function wrap(text, max) {
  const lines = [""];
  for (const w of text.split(" ")) {
    if ((lines[lines.length - 1] + " " + w).trim().length > max && lines[lines.length - 1]) lines.push(w);
    else lines[lines.length - 1] = (lines[lines.length - 1] + " " + w).trim();
  }
  if (lines.length > 2) lines[1] = lines[1].slice(0, max - 1) + "…";
  return lines.slice(0, 2);
}

function currentTarget() {
  const stored = state.plan.next_node_id;
  if (stored) return { id: stored, source: "set by you", label: nodeById[stored].name };
  return { id: catalog.default_target, source: "default from ROADMAP.md", label: catalog.default_target_label || nodeById[catalog.default_target].name };
}

// "Lab path completed" = nodes that have exercise folders (catalog overlay); this is NOT mastery.
const isCovered = (n) => n.exercises.length > 0;

function mapSvg(selectedId) {
  const L = layout();
  const here = currentTarget().id;
  const svg = sv("svg", { class: "map", width: L.width, height: L.height, viewBox: `0 0 ${L.width} ${L.height}`,
    role: "img", "aria-label": "Knowledge map" });
  for (const a of catalog.areas) {
    svg.append(sv("rect", { class: "lane" + (a.planned ? " planned" : ""), x: L.colX[a.id], y: 4, width: L.colW[a.id], height: L.height - 8, rx: 10 }),
      sv("text", { class: "lane-title", x: L.colX[a.id] + 10, y: 22 }, a.name),
      sv("text", { class: "lane-sub", x: L.colX[a.id] + 10, y: 37 }, (a.phase || "") + (a.planned ? " · planned" : "")));
  }
  const linked = new Set(selectedId ? [...nodeById[selectedId].prerequisites, ...catalog.nodes.filter((n) => n.prerequisites.includes(selectedId)).map((n) => n.id)] : []);
  const edges = [];
  for (const n of catalog.nodes) for (const p of n.prerequisites) {
    const a = L.pos[p], b = L.pos[n.id];
    const x1 = a.x + NW / 2, y1 = a.y + NH, x2 = b.x + NW / 2, y2 = b.y, my = (y1 + y2) / 2;
    const hot = selectedId && (p === selectedId || n.id === selectedId);
    const done = isCovered(nodeById[p]) && isCovered(n);
    edges.push(sv("path", { class: "edge" + (done ? " done" : "") + (p === here ? " next" : "") + (hot ? " hot" : ""), d: `M${x1},${y1} C${x1},${my} ${x2},${my} ${x2},${y2}` }));
  }
  // plain edges first, completed path and highlighted edges on top
  edges.sort((a, b) => a.getAttribute("class").length - b.getAttribute("class").length).forEach((e) => svg.append(e));
  for (const n of catalog.nodes) {
    const { x, y } = L.pos[n.id], st = statusOf(n.id), area = catalog.areas.find((a) => a.id === n.area);
    const g = sv("g", { class: `node st-${st}` + (area.planned ? " planned" : "") + (isCovered(n) ? " covered" : "") + (n.id === here ? " current" : "") + (n.id === selectedId ? " selected" : "") + (linked.has(n.id) ? " linked" : ""),
      tabindex: "0", role: "button",
      "aria-label": `${n.name}: ${STATUS_LABEL[st]}${isCovered(n) ? ", lab path completed" : ""}${n.id === here ? ", current target" : ""}` });
    g.addEventListener("click", () => (location.hash = "#/node/" + n.id));
    g.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); location.hash = "#/node/" + n.id; } });
    g.append(sv("title", {}, `${n.name} — ${STATUS_LABEL[st]}${isCovered(n) ? " · lab path completed" : ""}`),
      sv("rect", { class: "box", x, y, width: NW, height: NH, rx: 7 }),
      isCovered(n) ? sv("rect", { class: "cover-bar", x: x + 1, y: y + NH - 4, width: NW - 2, height: 3, rx: 1.5 }) : null,
      wrap(n.name, 21).map((line, i) => sv("text", { class: "label", x: x + 8, y: y + 16 + i * 13 }, line)),
      sv("text", { class: "glyph", x: x + NW - 8, y: y + 16, "text-anchor": "end" }, GLYPH[st]));
    if (n.id === here) {
      g.append(sv("rect", { class: "glow", x: x - 3, y: y - 3, width: NW + 6, height: NH + 6, rx: 10 }),
        sv("rect", { class: "here-pill", x: x + NW / 2 - 50, y: y - 21, width: 100, height: 16, rx: 8 }),
        sv("text", { class: "here-text", x: x + NW / 2, y: y - 9.5, "text-anchor": "middle" }, "YOU ARE HERE"));
    }
    svg.append(g);
  }
  return svg;
}

function legend() {
  const key = (cls, glyph, text) => h("span", { class: "key " + cls }, h("b", {}, glyph), " " + text);
  return h("div", { class: "legend" },
    h("span", { class: "legend-title" }, "Mastery"),
    Object.entries(STATUS_LABEL).map(([s, l]) => key("st-" + s, GLYPH[s], l)),
    h("span", { class: "legend-title" }, "Map"),
    key("cov", "▬", "lab path completed"),
    key("here", "▾", "current target"),
    key("fade", "◌", "planned future area"));
}

function banner() {
  const t = currentTarget(), done = catalog.completed_through;
  return h("div", { class: "banner" },
    h("div", { class: "chip done" }, h("span", { class: "chip-k" }, "Completed through"), h("strong", {}, done.label)),
    h("div", { class: "chip target" }, h("span", { class: "chip-k" }, "Current target"), h("strong", {}, t.label), h("span", { class: "muted" }, t.source)),
    h("p", { class: "muted note" }, "Topics are knowledge domains; ROADMAP.md is the route. “Lab path completed” means the learning path has reached this content (it has exercises), not that you master it. Mastery is your own rating below."));
}

function mapView(selectedId, panel) {
  const close = () => { location.hash = "#/"; };
  return h("div", {}, banner(), legend(),
    h("div", { class: "mapcols" }, h("div", { class: "mapwrap" + (panel ? " drawer-open" : "") }, mapSvg(selectedId)),
      panel ? h("aside", { class: "panel drawer", "aria-label": "Concept details" },
        h("button", { type: "button", class: "close", "aria-label": "Close details", onclick: close }, "×"), panel) : null),
    panel ? null : h("p", { class: "muted hint" }, "Select a concept to inspect it, rate your mastery, add evidence or set it as your current target."));
}

async function nodePanel(id) {
  const node = nodeById[id];
  const { evidence } = await api("/api/nodes/" + encodeURIComponent(id));
  const dependents = catalog.nodes.filter((n) => n.prerequisites.includes(id));
  const list = (ids) => ids.length ? h("ul", { class: "plain" }, ids.map((p) => h("li", {}, nodeLink(p), " ", badge(statusOf(p))))) : h("p", { class: "muted" }, "None.");
  const isHere = currentTarget().id === id;
  const section = (title, ...body) => h("section", {}, h("h3", {}, title), body);
  return h("div", {},
    h("h2", {}, node.name),
    h("p", { class: "tags" }, badge(statusOf(id)),
      isCovered(node) ? h("span", { class: "badge cov" }, "lab path completed") : null,
      isHere ? h("span", { class: "badge here" }, "current target") : null),
    h("p", {}, node.description),
    h("p", { class: "muted" }, catalog.areas.find((a) => a.id === node.area).name + (node.planned ? " · no exercises yet" : "")),
    section("Mastery (your rating)",
      formWith([h("select", { name: "status" }, Object.entries(STATUS_LABEL).map(([v, l]) =>
        h("option", { value: v, selected: v === statusOf(id) }, l)))], "Update",
        (f) => api(`/api/nodes/${id}/status`, { status: f.get("status") })),
      h("p", { class: "muted" }, "“Validated” needs at least one piece of evidence."),
      isHere ? null : h("button", { type: "button", class: "secondary", onclick: async () => { await api("/api/plan", { next_node_id: id }); await render(); } }, "Set as current target")),
    section("Prerequisites", list(node.prerequisites)),
    dependents.length ? section("Leads to", list(dependents.map((d) => d.id))) : null,
    node.related.length ? section("Related", list(node.related)) : null,
    section("Exercises", node.exercises.length ? h("ul", { class: "plain" }, node.exercises.map((e) => {
      const ex = exerciseById[e];
      return h("li", {}, ex.title, h("br"), h("code", {}, ex.path), " ", h("code", {}, "python " + ex.entrypoint));
    })) : h("p", { class: "muted" }, "No exercise exists yet.")),
    section("Repository resources", h("ul", { class: "plain" }, node.resources.map((r) => h("li", {}, r.title, " — ", h("code", {}, r.path || r.url))))),
    section("Evidence",
      evidence.length ? h("ul", { class: "plain" }, evidence.map((ev) => h("li", {},
        h("strong", {}, ev.kind), ": ", ev.text, ev.ref ? [" ", h("code", {}, ev.ref)] : null, " ", h("span", { class: "muted" }, fmt(ev.created_at)))))
        : h("p", { class: "muted" }, "No evidence recorded."),
      h("p", { class: "muted" }, "A passing test is evidence about code, not proof you understand the concept."),
      formWith([h("select", { name: "kind" }, KINDS.map((k) => h("option", { value: k }, k))),
                h("input", { type: "text", name: "text", placeholder: "What shows you understand this?" }),
                h("input", { type: "text", name: "ref", placeholder: "Optional repo path" })],
        "Add evidence", (f) => api(`/api/nodes/${id}/evidence`, { kind: f.get("kind"), text: f.get("text"), ref: f.get("ref") }))));
}

async function render() {
  const app = document.getElementById("app");
  const old = app.querySelector(".mapwrap");
  const keep = old ? [old.scrollLeft, old.scrollTop] : null;
  try {
    await load();
    const hash = location.hash || "#/";
    const m = hash.match(/^#\/node\/([\w.-]+)$/);
    const selected = m && nodeById[m[1]] ? m[1] : null;
    const isMap = hash === "#/" || hash === "#/map" || !!m;
    document.getElementById("nav-map").classList.toggle("active", isMap);
    document.getElementById("nav-dashboard").classList.toggle("active", !isMap);
    app.replaceChildren(isMap ? mapView(selected, selected ? await nodePanel(selected) : null) : dashboard());
    const wrapEl = app.querySelector(".mapwrap");
    if (wrapEl) {
      if (keep) { wrapEl.scrollLeft = keep[0]; wrapEl.scrollTop = keep[1]; }
      else {
        const cur = wrapEl.querySelector(".node.current .box");
        if (cur) {
          const b = cur.getBBox();
          wrapEl.scrollTop = Math.max(0, b.y + b.height / 2 - wrapEl.clientHeight / 2);
          wrapEl.scrollLeft = Math.max(0, b.x + b.width / 2 - wrapEl.clientWidth / 2);
        }
      }
    }
  } catch (e) {
    app.replaceChildren(h("p", { class: "error" }, "Error: " + e.message));
  }
}

window.addEventListener("hashchange", render);
window.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && /^#\/node\//.test(location.hash)) location.hash = "#/"; });
render();
