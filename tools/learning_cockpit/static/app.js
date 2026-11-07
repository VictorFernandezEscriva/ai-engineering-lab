"use strict";
// All dynamic text goes through textContent (via h), never innerHTML.
const STATUS_LABEL = { pending: "Pending", studying: "Studying", practiced: "Practiced", validated: "Validated" };
let catalog, state, nodeById, exerciseById, areaById, contentSet;
let mapMode = "overview"; // "overview" | "detail" | "phase:<area id>"; where the concept drawer was opened from

function h(tag, attrs, ...children) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else if (v !== false && v != null) el.setAttribute(k, v);
  }
  for (const c of children.flat(Infinity)) if (c != null) el.append(c);
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
const trackName = (id) => (catalog.tracks.find((t) => t.id === id) || { name: id }).name;
const trackShort = (id) => (catalog.tracks.find((t) => t.id === id) || { short: id }).short;
const nodeLink = (id) => h("a", { href: "#/node/" + id }, nodeById[id] ? nodeById[id].name : id);
// Catalog titles come from each README heading, which may already carry "Experiment NN — "; the number shown is always the derived global one.
const expLabel = (ex) => `Experiment ${ex.number} — ${ex.title.replace(/^Experiment \d+\s*[—–-]\s*/, "")}`;
const fmt = (iso) => (iso ? new Date(iso).toLocaleString() : "—");

async function load() {
  [catalog, state] = await Promise.all([api("/api/catalog"), api("/api/state")]);
  nodeById = Object.fromEntries(catalog.nodes.map((n) => [n.id, n]));
  exerciseById = Object.fromEntries(catalog.exercises.map((e) => [e.id, e]));
  areaById = Object.fromEntries(catalog.areas.map((a) => [a.id, a]));
  contentSet = new Set(catalog.content_paths);
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
      return h("div", { class: "card" }, h("strong", {}, h("a", { href: "#/phase/" + a.id }, a.name)), h("p", { class: "muted" }, firstSentence(a.purpose)),
        h("p", {}, `${ns.length} nodes · ${exs} exercises · ${ns.filter((n) => statusOf(n.id) === "validated").length} validated`));
    })),
    h("h2", {}, "Theory coverage"),
    h("div", { class: "card" }, Object.keys(THEORY_LABEL).map((s) => h("span", {}, h("span", { class: "badge theory-" + s }, THEORY_LABEL[s]), " ",
      String(catalog.nodes.filter((n) => n.content_status === s).length), " ")),
      h("p", { class: "muted" }, "Theory is written when a phase begins; planned means honestly not written yet.")),
    h("h2", {}, "Curriculum targets by professional role"),
    h("div", { class: "card" }, h("p", { class: "muted" }, "Which concepts a role draws on. These are curriculum targets and your own ratings, not job readiness."),
      (catalog.roles || []).map((r) => {
        const ids = new Set(catalog.nodes.filter((n) => r.areas.includes(n.area)).map((n) => n.id));
        catalog.capabilities.filter((c) => r.capabilities.includes(c.id)).forEach((c) => c.nodes.forEach((n) => ids.add(n)));
        const ns = catalog.nodes.filter((n) => ids.has(n.id));
        const rated = ns.filter((n) => ["practiced", "validated"].includes(statusOf(n.id))).length;
        return h("details", {}, h("summary", {}, h("strong", {}, r.name), ` — ${ns.length} concepts · ${ns.filter(isCovered).length} on the lab path · ${rated} rated practiced+`),
          h("p", { class: "muted" }, "Capabilities: " + catalog.capabilities.filter((c) => r.capabilities.includes(c.id)).map((c) => c.name).join(", ")),
          h("ul", { class: "plain" }, ns.map((n) => h("li", {}, nodeLink(n.id), " ", badge(statusOf(n.id))))));
      })),
    h("h2", {}, "Documents (one canonical responsibility each)"),
    h("div", { class: "card" }, h("ul", { class: "plain" }, (catalog.documents || []).map((d) => h("li", {},
      h("a", { href: docHref(d.path) }, d.title), " — ", h("span", { class: "muted" }, d.role))))),
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

// Node.append() would stringify arrays and "null"; this flattens and skips empty children (labels were silently dropped before).
const put = (el, ...c) => { for (const x of c.flat()) if (x != null) el.append(x); return el; };
const SVG_NS = "http://www.w3.org/2000/svg";
function sv(tag, attrs, ...children) {
  const el = document.createElementNS(SVG_NS, tag);
  for (const [k, v] of Object.entries(attrs || {})) if (v != null && v !== false) el.setAttribute(k, v);
  for (const c of children.flat()) if (c != null) el.append(c);
  return el;
}

const NW = 152, NH = 40, GAP = 8, ROW = 52, TOP = 50, PAD = 10;
const GLYPH = { pending: "○", studying: "◔", practiced: "◑", validated: "✓" };
const THEORY_LABEL = { available: "Theory available", partial: "Partial theory", implied: "Theory implied by an experiment", planned: "Theory: planned (not written yet)" };

// A view is the set of nodes a map draws: the whole catalog (Detailed) or one phase plus its direct neighbours.
function makeView(nodes, areas, focus) {
  const inView = new Set(nodes.map((n) => n.id));
  const edges = [];
  for (const n of nodes) for (const p of n.prerequisites) {
    if (inView.has(p) && (!focus || n.area === focus || nodeById[p].area === focus)) edges.push([p, n.id]);
  }
  return { nodes, areas, focus, edges, inView };
}
const fullView = () => makeView(catalog.nodes, catalog.areas, null);
function phaseView(areaId) {
  const own = new Set(catalog.nodes.filter((n) => n.area === areaId).map((n) => n.id));
  const keep = catalog.nodes.filter((n) => own.has(n.id) || n.prerequisites.some((p) => own.has(p)) ||
    [...own].some((o) => nodeById[o].prerequisites.includes(n.id)));
  const used = new Set(keep.map((n) => n.area));
  return makeView(keep, catalog.areas.filter((a) => used.has(a.id)), areaId);
}

// Lane layout, computed from the catalog. Columns = areas (route order). Inside a lane, rows follow the
// lane's own prerequisite chain. Each lane is then shifted down only as far as needed so that its
// cross-lane prerequisites sit above it.
function layout(view) {
  const nodes = view.nodes;
  const preds = Object.fromEntries(nodes.map((n) => [n.id, []]));
  view.edges.forEach(([p, n]) => preds[n].push(p));
  const local = {};
  const localDepth = (id) => local[id] ?? (local[id] = Math.max(-1, ...preds[id]
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
      for (const p of preds[n.id]) {
        if (nodeById[p].area !== area) s = Math.max(s, placed(p) + 1 - local[n.id]);
      }
    }
    return (shift[area] = s);
  };
  view.areas.forEach((a) => laneShift(a.id));
  nodes.forEach((n) => placed(n.id));
  const groups = {};
  nodes.forEach((n) => { const k = n.area + "|" + row[n.id]; (groups[k] = groups[k] || []).push(n.id); });
  const colX = {}, colW = {};
  let x = PAD;
  for (const a of view.areas) {
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

function wrap(text, max, maxLines = 2) {
  const lines = [""];
  for (const w of text.split(" ")) {
    if ((lines[lines.length - 1] + " " + w).trim().length > max && lines[lines.length - 1]) lines.push(w);
    else lines[lines.length - 1] = (lines[lines.length - 1] + " " + w).trim();
  }
  if (lines.length > maxLines) lines[maxLines - 1] = lines[maxLines - 1].slice(0, Math.max(1, max - 1)).trimEnd() + "…";
  return lines.slice(0, maxLines);
}

function currentTarget() {
  const stored = state.plan.next_node_id;
  if (stored) return { id: stored, source: "set by you", label: nodeById[stored].name };
  return { id: catalog.default_target, source: "default from ROADMAP.md", label: catalog.default_target_label || nodeById[catalog.default_target].name };
}

// "Lab path completed" = nodes that have exercise folders (catalog overlay); this is NOT mastery.
const isCovered = (n) => n.exercises.length > 0;

// Prerequisites of the current target that the lab path has not reached yet ("what do I need next?"), derived only.
function neededForTarget() {
  const out = new Set();
  const walk = (id) => nodeById[id].prerequisites.forEach((p) => { if (!out.has(p)) { out.add(p); walk(p); } });
  walk(currentTarget().id);
  return new Set([...out].filter((id) => !isCovered(nodeById[id])));
}

function mapSvg(selectedId, view) {
  const L = layout(view);
  const here = currentTarget().id;
  const needed = neededForTarget();
  const svg = sv("svg", { class: "map", width: L.width, height: L.height, viewBox: `0 0 ${L.width} ${L.height}`,
    role: "img", "aria-label": "Knowledge map" });
  for (const a of view.areas) {
    svg.append(sv("rect", { class: "lane track-" + a.track + (a.planned ? " planned" : ""), x: L.colX[a.id], y: 4, width: L.colW[a.id], height: L.height - 8, rx: 10 }),
      sv("text", { class: "lane-title", x: L.colX[a.id] + 10, y: 22 }, a.name),
      sv("text", { class: "lane-sub", x: L.colX[a.id] + 10, y: 37 }, (a.phase || "") + " · " + trackShort(a.track) + (a.planned ? " · planned" : "")));
  }
  const linked = new Set(selectedId ? [...nodeById[selectedId].prerequisites, ...catalog.nodes.filter((n) => n.prerequisites.includes(selectedId)).map((n) => n.id)] : []);
  const edges = [];
  for (const [p, nid] of view.edges) {
    const a = L.pos[p], b = L.pos[nid];
    const x1 = a.x + NW / 2, y1 = a.y + NH, x2 = b.x + NW / 2, y2 = b.y, my = (y1 + y2) / 2;
    const hot = selectedId && (p === selectedId || nid === selectedId);
    const done = isCovered(nodeById[p]) && isCovered(nodeById[nid]);
    edges.push(sv("path", { class: "edge" + (done ? " done" : "") + (p === here ? " next" : "") + (hot ? " hot" : ""), d: `M${x1},${y1} C${x1},${my} ${x2},${my} ${x2},${y2}` }));
  }
  // plain edges first, completed path and highlighted edges on top
  edges.sort((a, b) => a.getAttribute("class").length - b.getAttribute("class").length).forEach((e) => svg.append(e));
  for (const n of view.nodes) {
    const { x, y } = L.pos[n.id], st = statusOf(n.id), area = areaById[n.area];
    const g = sv("g", { class: `node st-${st}` + (area.planned ? " planned" : "") + (isCovered(n) ? " covered" : "") + (n.id === here ? " current" : "") + (n.id === selectedId ? " selected" : "") + (linked.has(n.id) ? " linked" : "") + (needed.has(n.id) ? " needed" : "") + (view.focus && n.area !== view.focus ? " ext" : ""),
      tabindex: "0", role: "button",
      "aria-label": `${n.name}: ${STATUS_LABEL[st]}${isCovered(n) ? ", lab path completed" : ""}${n.id === here ? ", current target" : ""}` });
    g.addEventListener("click", () => (location.hash = "#/node/" + n.id));
    g.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); location.hash = "#/node/" + n.id; } });
    put(g, sv("title", {}, `${n.name} — ${STATUS_LABEL[st]}${isCovered(n) ? " · lab path completed" : ""} · ${THEORY_LABEL[n.content_status]}`),
      sv("rect", { class: "box", x, y, width: NW, height: NH, rx: 7 }),
      isCovered(n) ? sv("rect", { class: "cover-bar", x: x + 1, y: y + NH - 4, width: NW - 2, height: 3, rx: 1.5 }) : null,
      wrap(n.name, 21).map((line, i) => sv("text", { class: "label", x: x + 8, y: y + 16 + i * 13 }, line)),
      sv("text", { class: "glyph", x: x + NW - 8, y: y + 16, "text-anchor": "end" }, GLYPH[st]));
    if (n.id === here) {
      put(g, sv("rect", { class: "glow", x: x - 3, y: y - 3, width: NW + 6, height: NH + 6, rx: 10 }),
        sv("rect", { class: "here-pill", x: x + NW - 78, y: y - 7, width: 74, height: 12, rx: 6 }),
        sv("text", { class: "here-text", x: x + NW - 41, y: y + 2, "text-anchor": "middle", style: "font-size:8px;letter-spacing:0" }, "YOU ARE HERE"));
    }
    svg.append(g);
  }
  return svg;
}

// ---- LEVEL 1: the 17 phases, derived entirely from the catalog (areas with a topic path + cross-area prerequisites) ----
const clampN = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
const firstSentence = (t) => { const m = (t || "").match(/^.*?[.!?](\s|$)/); return (m ? m[0] : t || "").trim(); };
// Room the map may use: the app column width, and the window height below the page chrome.
function availableMapSize() {
  const app = document.getElementById("app");
  return { w: Math.max(640, (app ? app.clientWidth : window.innerWidth) - 4), h: Math.max(420, window.innerHeight - 190) };
}
const phaseState = (a, here) => (a.id === here ? "In progress" : a.planned ? "Planned" : "Lab path completed");

function overviewSvg() {
  const phases = catalog.areas.filter((a) => a.path);
  const cross = catalog.areas.filter((a) => !a.path);
  const preds = Object.fromEntries(phases.map((a) => [a.id, new Set()]));
  for (const n of catalog.nodes) for (const p of n.prerequisites) {
    const a = nodeById[p].area, b = n.area;
    if (a !== b && preds[a] && preds[b]) preds[b].add(a);
  }
  const depth = {};
  const dep = (id) => depth[id] ?? (depth[id] = (depth[id] = 0, Math.max(-1, ...[...preds[id]].map(dep)) + 1));
  phases.forEach((a) => dep(a.id));
  const COLS = ["core", "bridge", "applied"]; // presentation only: Track A | bridge | Track B
  const cell = {}, perTrack = { core: 1, bridge: 1, applied: 1 };
  for (const a of phases) {
    const k = a.track + "|" + depth[a.id];
    (cell[k] = cell[k] || []).push(a.id);
    perTrack[a.track] = Math.max(perTrack[a.track] || 1, cell[k].length);
  }
  // Fit: card width fills the available width; type scales gently with it; row pitch uses the height when it can.
  const avail = availableMapSize();
  const nCols = COLS.reduce((n, t) => n + perTrack[t], 0), rows = Math.max(...Object.values(depth)) + 1;
  // Natural size first; if the 9 stacked rows are taller than the window, scale the whole drawing down
  // (never below 90%) and widen the virtual canvas so the width is still filled.
  const G = 14, TG = 22, VG = 12, f = 1.05;
  const HEAD = Math.round(60 * f), CROSSH = Math.round(40 * f), OH = Math.round(88 * f);
  const natural = HEAD + rows * (OH + VG) + CROSSH + 34;
  const scale = clampN(avail.h / natural, 0.9, 1);
  const OW = clampN((avail.w / scale - 2 * PAD - nCols * G - (COLS.length - 1) * TG) / nCols, 190, 420);
  const colX = {};
  let x = PAD;
  for (const t of COLS) { colX[t] = x; x += perTrack[t] * (OW + G) + TG - G; }
  const crossY = HEAD + rows * (OH + VG) + 4;
  const width = x - TG + G + PAD, height = crossY + CROSSH + 14;
  const svg = sv("svg", { class: "map overview", width: width * scale, height: height * scale, viewBox: `0 0 ${width} ${height}`, role: "img", "aria-label": "Global AI Engineering map" });
  const pos = {};
  for (const [k, ids] of Object.entries(cell)) {
    const [t, d] = k.split("|");
    ids.sort((a, b) => phases.findIndex((p) => p.id === a) - phases.findIndex((p) => p.id === b))
      .forEach((id, i) => (pos[id] = { x: colX[t] + i * (OW + G), y: HEAD + Number(d) * (OH + VG) }));
  }
  const fs = (px) => ({ style: `font-size:${(px * f).toFixed(1)}px` });
  for (const t of COLS) {
    const tr = catalog.tracks.find((r) => r.id === t);
    put(svg, sv("rect", { class: "lane track-" + t, x: colX[t] - 6, y: 4, width: perTrack[t] * (OW + G) + 2, height: crossY - 8, rx: 10 }),
      sv("text", { class: "lane-title track-head", x: colX[t] + 4, y: 24 * f, ...fs(13) }, tr.name.toUpperCase()),
      wrap(tr.description, Math.floor((perTrack[t] * (OW + G) - 12) / (6.2 * f)), 2).map((l, i) => sv("text", { class: "lane-sub", x: colX[t] + 4, y: 40 * f + i * 12 * f, ...fs(10.5) }, l)));
  }
  const edges = [];
  for (const b of phases) for (const a of preds[b.id]) {
    const p = pos[a], q = pos[b.id];
    const x1 = p.x + OW / 2, y1 = p.y + OH, x2 = q.x + OW / 2, y2 = q.y, my = (y1 + y2) / 2;
    edges.push(sv("path", { class: "edge", d: `M${x1},${y1} C${x1},${my} ${x2},${my} ${x2},${y2}` }));
  }
  edges.forEach((e) => svg.append(e));
  const here = areaById[nodeById[currentTarget().id].area].id;
  const first = Object.fromEntries(COLS.map((t) => [t, phases.find((a) => a.track === t)]));
  const last = phases[phases.length - 1];
  const open = (id) => { location.hash = "#/phase/" + id; };
  const phaseBox = (a, x0, y0, w, h0, wide) => {
    const ns = catalog.nodes.filter((n) => n.area === a.id);
    const ex = ns.filter(isCovered).length, rated = ns.filter((n) => ["practiced", "validated"].includes(statusOf(n.id))).length;
    const theory = ns.filter((n) => n.content_status !== "planned").length;
    const nExp = catalog.exercises.filter((e) => e.area === a.id).length;
    const st = phaseState(a, here);
    const g = sv("g", { class: "phase" + (a.planned ? " planned" : "") + (a.id === here ? " current" : "") + (ex ? " covered" : ""), tabindex: "0", role: "button",
      "aria-label": `${a.phase} ${a.name}: ${st}, ${ns.length} concepts` });
    g.addEventListener("click", () => open(a.id));
    g.addEventListener("keydown", (ev) => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); open(a.id); } });
    const nameLines = wrap(a.name, Math.floor((w - 20) / (7.9 * f)), 2);
    const purposeLines = wrap(firstSentence(a.purpose), Math.floor((w - 20) / (6.9 * f)), wide ? 1 : 2);
    const lh = 14 * f;
    put(g, sv("title", {}, `${a.phase} — ${a.name} (${st})\n${firstSentence(a.purpose)}\n${ns.length} concepts · ${nExp} experiments · ${theory} with theory · ${rated} rated practiced+`),
      sv("rect", { class: "box", x: x0, y: y0, width: w, height: h0, rx: 9 }),
      sv("text", { class: "lane-sub ph-meta", x: x0 + 10, y: y0 + 15 * f, ...fs(10.5) }, `${a.phase.toUpperCase()} · ${trackShort(a.track).toUpperCase()} · ${st.toUpperCase()}`),
      nameLines.map((l, i) => sv("text", { class: "label ph-name", x: x0 + 10, y: y0 + 32 * f + i * lh, ...fs(13.5) }, l)),
      purposeLines.map((l, i) => sv("text", { class: "ph-purpose", x: x0 + 10, y: y0 + 33 * f + nameLines.length * lh + 2 + i * 14 * f, ...fs(10.5) }, l)),
      sv("text", { class: "lane-sub ph-counts", x: x0 + 10, y: y0 + h0 - 9, ...fs(10.5) },
        `${ns.length} concepts · ${nExp ? nExp + " experiment" + (nExp > 1 ? "s" : "") : "no experiments yet"} · ${theory ? "theory " + theory + "/" + ns.length : "theory planned"}`),
      ex ? sv("rect", { class: "cover-bar", x: x0 + 1, y: y0 + h0 - 4, width: Math.max(4, (w - 2) * ex / ns.length), height: 3, rx: 1.5 }) : null);
    if (a.id === here) {
      put(g, sv("rect", { class: "glow", x: x0 - 3, y: y0 - 3, width: w + 6, height: h0 + 6, rx: 12 }),
        sv("rect", { class: "here-pill", x: x0 + 10, y: y0 - 21, width: 100, height: 16, rx: 8 }),
        sv("text", { class: "here-text", x: x0 + 60, y: y0 - 9.5, "text-anchor": "middle" }, "YOU ARE HERE"));
    }
    const tags = [];
    if (a === first[a.track] && a.track !== "bridge") tags.push(a.track === "core" ? "TRACK A STARTS" : "TRACK B STARTS");
    if (a === last) tags.push("TRACKS CONVERGE");
    tags.forEach((tg) => put(g, sv("rect", { class: "tag-pill", x: x0 + w - 8 - 104, y: y0 - 14, width: 104, height: 15, rx: 7.5 }),
      sv("text", { class: "tag-text", x: x0 + w - 8 - 52, y: y0 - 3.5, "text-anchor": "middle" }, tg)));
    return g;
  };
  for (const a of phases) svg.append(phaseBox(a, pos[a.id].x, pos[a.id].y, OW, OH, false));
  cross.forEach((a) => svg.append(phaseBox(a, PAD, crossY, width - 2 * PAD, CROSSH, true)));
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
    key("need", "◇", "needed next"),
    key("fade", "◌", "planned"),
    h("span", { class: "legend-title" }, "Track"),
    catalog.tracks.filter((t) => t.id !== "cross-cutting").map((t) => h("span", { class: "key trk-" + t.id }, h("b", {}, "■"), " " + t.short)),
    h("details", { class: "help" }, h("summary", {}, "What do these mean?"),
      h("dl", {},
        h("dt", {}, "Mastery"), h("dd", {}, "How well YOU know the concept. You set it; passing tests does not change it."),
        h("dt", {}, "Lab path completed"), h("dd", {}, "An experiment exists for it and the learning path has reached it. Not a claim that you master it."),
        h("dt", {}, "Current target"), h("dd", {}, "What the roadmap says to study next."),
        h("dt", {}, "Needed next"), h("dd", {}, "A prerequisite of the current target that the lab path has not reached yet."),
        h("dt", {}, "Planned"), h("dd", {}, "Future curriculum: not written or practiced yet."),
        h("dt", {}, "Track"), h("dd", {}, "Core AI Engineering (Track A), Applied AI Automation & Agentic Systems (Track B), and the Bridge where they meet."))));
}

function banner() {
  const t = currentTarget(), done = catalog.completed_through;
  return h("div", { class: "banner" },
    h("div", { class: "chip done" }, h("span", { class: "chip-k" }, "Completed through"), h("strong", {}, done.label)),
    h("div", { class: "chip target" }, h("span", { class: "chip-k" }, "Current target"), h("strong", {}, t.label), h("span", { class: "muted" }, t.source)),
    h("p", { class: "muted note" }, "One ordered journey (ROADMAP.md), two tracks. Mastery is your own rating; “lab path completed” only means an experiment exists."));
}

const modeHash = () => (mapMode === "detail" ? "#/detail" : mapMode.startsWith("phase:") ? "#/" + mapMode.replace(":", "/") : "#/");

function breadcrumb() {
  const crumbs = [h("a", { href: "#/" }, "Atlas")];
  if (mapMode.startsWith("phase:")) {
    const a = areaById[mapMode.slice(6)];
    crumbs.push(" › ", h("strong", {}, (a.phase && a.path ? a.phase + " — " : "") + a.name));
  } else if (mapMode === "detail") crumbs.push(" › ", h("strong", {}, "Detailed map (all concepts)"));
  else crumbs.push(" › ", h("strong", {}, "Overview (17 phases)"));
  crumbs.push(h("span", { class: "spacer" }), h("a", { href: "#/" , class: mapMode === "overview" ? "tab on" : "tab" }, "Overview"),
    h("a", { href: "#/detail", class: mapMode === "detail" ? "tab on" : "tab" }, "Detailed"));
  return h("div", { class: "crumbs" }, crumbs);
}

// Phases other phases' concepts depend on / that depend on this one, derived from the concept graph.
function phaseNeighbours(areaId) {
  const before = new Set(), after = new Set();
  for (const n of catalog.nodes) for (const p of n.prerequisites) {
    const pa = nodeById[p].area;
    if (pa === n.area) continue;
    if (n.area === areaId) before.add(pa);
    if (pa === areaId) after.add(n.area);
  }
  const named = (set) => catalog.areas.filter((a) => set.has(a.id) && a.path);
  return { before: named(before), after: named(after) };
}

function phaseHeader(areaId, open) {
  const a = areaById[areaId], ns = catalog.nodes.filter((n) => n.area === areaId);
  const nExp = catalog.exercises.filter((e) => e.area === areaId).length;
  const theory = ns.filter((n) => n.content_status !== "planned").length;
  const { before, after } = phaseNeighbours(areaId);
  const here = areaById[nodeById[currentTarget().id].area].id;
  const st = phaseState(a, here);
  const phaseLinks = (list) => list.length ? list.map((x, i) => [i ? ", " : "", h("a", { href: "#/phase/" + x.id }, `${x.phase} ${x.name}`)]) : h("span", { class: "muted" }, "none");
  const item = (k, ...body) => h("div", { class: "ph-item" }, h("span", { class: "ph-k" }, k), body);
  return h("details", { class: "card phasehead", open: open ? "" : false },
    h("summary", {}, h("strong", {}, (a.path ? a.phase + " — " : "") + a.name), " ", h("span", { class: "badge planned" }, trackName(a.track)), " ",
      h("span", { class: "badge " + (a.id === here ? "here" : a.planned ? "planned" : "cov") }, st)),
    h("div", { class: "ph-grid" },
      item("What this phase is", a.purpose),
      a.why ? item("Why it matters", a.why) : null,
      item("What you will learn", ns.slice(0, 5).map((n) => n.name).join(" · ") + (ns.length > 5 ? ` · +${ns.length - 5} more (shown in the map below)` : "")),
      item("Where it fits", `${trackName(a.track)}. Comes after: `, phaseLinks(before), ". Leads to: ", phaseLinks(after), "."),
      item("Status", `${st} · ${ns.length} concepts · ${nExp ? nExp + " experiment" + (nExp > 1 ? "s" : "") : "no experiments yet"} · theory ${theory ? theory + " of " + ns.length : "planned"}`)),
    h("p", { class: "muted ph-foot" },
      a.path ? [h("a", { class: "btn", href: docHref(a.path + "/README.md") }, "Open phase overview"), " "] : null,
      "Faded concepts belong to neighbouring phases."));
}

function mapView(selectedId, panel) {
  const mode = mapMode;
  let svg, extra = null;
  if (mode === "overview") svg = overviewSvg();
  else if (mode === "detail") svg = mapSvg(selectedId, fullView());
  else { svg = mapSvg(selectedId, phaseView(mode.slice(6))); extra = phaseHeader(mode.slice(6), !panel); }
  const close = () => { location.hash = modeHash(); };
  return h("div", {}, banner(), breadcrumb(), mode === "overview" ? null : legend(), extra,
    h("div", { class: "mapcols" }, h("div", { class: "mapwrap" + (panel ? " drawer-open" : "") }, svg),
      panel ? h("aside", { class: "panel drawer", "aria-label": "Concept details" },
        h("button", { type: "button", class: "close", "aria-label": "Close details", onclick: close }, "×"), panel) : null),
    panel ? null : h("p", { class: "muted hint" }, mode === "overview"
      ? "Click a phase to see its purpose and concepts. Lines are prerequisites between phases; “Detailed” shows every concept at once."
      : mode === "detail" ? "Select a concept for what it is, why it matters, theory and experiments. Scroll sideways with the bar under the map, Shift+wheel or a trackpad."
      : "Select a concept for what it is, why it matters, theory and experiments."));
}

const resourcesFor = (id) => (catalog.resources || []).filter((r) => r.nodes.includes(id));
const technologiesFor = (id) => (catalog.technologies || []).filter((x) => x.nodes.includes(id));
const capabilitiesFor = (id) => (catalog.capabilities || []).filter((x) => x.nodes.includes(id));
const roadmapDoc = () => (catalog.documents || []).find((d) => d.id === "roadmap");
const docHref = (path) => "#/doc/" + encodeURIComponent(path);

// Where a concept sits relative to the learner's route. Three different things, never conflated:
// the roadmap's current target, what the lab path has reached, and the learner's own mastery rating.
function contextOf(id) {
  const node = nodeById[id], t = currentTarget();
  if (id === t.id) return { key: "here", label: "Current target", text: "This is what the roadmap says to study next." };
  if (isCovered(node)) return { key: "cov", label: "Lab path completed", text: "The learning path has reached this concept (an experiment exists). Your own mastery rating is separate and set below." };
  if (neededForTarget().has(id)) return { key: "need", label: "Needed for current target", text: `A prerequisite of your current target (${t.label}) that the lab path has not reached yet.` };
  return { key: "future", label: "Future curriculum", text: "Comes after your current target. Nothing here has been studied; theory and experiments are written when its phase begins." };
}

async function nodePanel(id) {
  const node = nodeById[id];
  const { evidence } = await api("/api/nodes/" + encodeURIComponent(id));
  const dependents = catalog.nodes.filter((n) => n.prerequisites.includes(id));
  const list = (ids) => ids.length ? h("ul", { class: "plain" }, ids.map((p) => h("li", {}, nodeLink(p), " ", badge(statusOf(p))))) : h("p", { class: "muted" }, "None.");
  const isHere = currentTarget().id === id;
  const area = areaById[node.area], ctx = contextOf(id);
  const caps = capabilitiesFor(id), techs = technologiesFor(id);
  const section = (title, ...body) => h("section", {}, h("h3", {}, title), body);
  const whyBits = [
    dependents.length ? h("p", {}, "Needed to understand: ", dependents.map((d, i) => [i ? ", " : "", nodeLink(d.id)])) : null,
    caps.length ? h("p", {}, "Supports professional capabilities: " + caps.map((x) => x.name).join(", ") + ".") : null,
    area.why ? h("p", { class: "muted" }, (area.path ? area.phase + ": " : "") + area.why) : null].filter(Boolean);
  return h("div", {},
    h("h2", {}, node.name),
    h("p", { class: "ctx" }, h("a", { href: "#/phase/" + area.id }, (area.path && area.phase ? area.phase + " — " : "") + area.name),
      " · " + trackName(node.track || area.track)),
    h("p", { class: "tags" }, h("span", { class: "badge ctx-" + ctx.key }, ctx.label), badge(statusOf(id))),
    section("What it is", h("p", {}, node.description)),
    section("Why it matters", whyBits.length ? whyBits : h("p", { class: "muted" }, "No dependants are recorded for this concept yet.")),
    section("Where you are", h("p", {}, ctx.text),
      isHere ? null : h("button", { type: "button", class: "secondary", onclick: async () => { await api("/api/plan", { next_node_id: id }); await render(); } }, "Set as current target")),
    section("What you need first", list(node.prerequisites)),
    section("Next concepts", list(dependents.map((d) => d.id))),
    node.related.length ? section("Related", list(node.related)) : null,
    section("Theory",
      h("p", {}, h("span", { class: "badge theory-" + node.content_status }, THEORY_LABEL[node.content_status])),
      node.content_path ? h("p", {}, h("a", { class: "btn", href: docHref(node.content_path) }, "Open theory"))
        : h("p", { class: "muted" }, "Written when this phase begins; the phase overview describes the intended scope."),
      area.path ? h("p", { class: "muted" }, h("a", { href: docHref(area.path + "/README.md") }, "Phase overview"), " · ", roadmapDoc() ? h("a", { href: docHref(roadmapDoc().path) }, "ROADMAP") : null) : null),
    section("Experiments", node.exercises.length ? h("ul", { class: "plain" }, node.exercises.map((e) => {
      const ex = exerciseById[e];
      return h("li", {}, h("strong", {}, expLabel(ex)), " ", h("a", { class: "btn", href: docHref(ex.readme) }, "Open experiment README"),
        h("details", {}, h("summary", { class: "muted" }, "Folder and run command"), h("code", {}, ex.path), " ", h("code", {}, "python " + ex.entrypoint)));
    })) : h("p", { class: "muted" }, "No experiment exists yet.")),
    techs.length ? section("Technologies", h("ul", { class: "plain" }, techs.map((x) => h("li", {},
      h("strong", {}, x.name), " ", h("span", { class: "badge" }, x.tier), h("br"), h("span", { class: "muted" }, x.purpose))))) : null,
    node.resources.length ? section("Other repository resources", h("ul", { class: "plain" }, node.resources.map((r) => h("li", {}, r.title, " — ",
      r.path && contentSet.has(r.path) ? h("a", { href: docHref(r.path) }, r.path) : h("code", {}, r.path || r.url))))) : null,
    resourcesFor(id).length ? section("Learning resources (external, free)", h("ul", { class: "plain" }, resourcesFor(id).map((r) => h("li", {},
      h("a", { href: r.url, target: "_blank", rel: "noopener noreferrer" }, r.name), " ", h("span", { class: "muted" }, r.provider),
      h("br"), h("span", { class: "muted" }, r.timing))))) : null,
    section("Mastery (your rating)",
      formWith([h("select", { name: "status" }, Object.entries(STATUS_LABEL).map(([v, l]) =>
        h("option", { value: v, selected: v === statusOf(id) }, l)))], "Update",
        (f) => api(`/api/nodes/${id}/status`, { status: f.get("status") })),
      h("p", { class: "muted" }, "“Validated” needs at least one piece of evidence.")),
    section("Evidence",
      evidence.length ? h("ul", { class: "plain" }, evidence.map((ev) => h("li", {},
        h("strong", {}, ev.kind), ": ", ev.text, ev.ref ? [" ", h("code", {}, ev.ref)] : null, " ", h("span", { class: "muted" }, fmt(ev.created_at)))))
        : h("p", { class: "muted" }, "No evidence recorded."),
      h("p", { class: "muted" }, "A passing test is evidence about code, not proof you understand the concept."),
      formWith([h("select", { name: "kind" }, catalog.evidence_kinds.map((k) => h("option", { value: k }, k))),
                h("input", { type: "text", name: "text", placeholder: "What shows you understand this?" }),
                h("input", { type: "text", name: "ref", placeholder: "Optional repo path" })],
        "Add evidence", (f) => api(`/api/nodes/${id}/evidence`, { kind: f.get("kind"), text: f.get("text"), ref: f.get("ref") }))));
}

// ---- read-only Markdown viewer: the file stays the source of truth; text only ever goes through textContent ----
function resolveRel(basePath, href) {
  const parts = basePath.split("/").slice(0, -1);
  for (const seg of href.split("#")[0].split("/")) {
    if (seg === "..") parts.pop();
    else if (seg && seg !== ".") parts.push(seg);
  }
  return parts.join("/");
}

function inline(text, basePath) {
  const out = [], re = /`([^`]+)`|\*\*([^*]+)\*\*|\[([^\]]+)\]\(([^)\s]+)[^)]*\)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(text.slice(last, m.index));
    if (m[1] !== undefined) out.push(h("code", {}, m[1]));
    else if (m[2] !== undefined) out.push(h("strong", {}, m[2]));
    else if (/^https:\/\//.test(m[4])) out.push(h("a", { href: m[4], target: "_blank", rel: "noopener noreferrer" }, m[3]));
    else {
      const target = m[4].startsWith("#") ? null : resolveRel(basePath, m[4]);
      out.push(target && contentSet.has(target) ? h("a", { href: docHref(target) }, m[3]) : h("span", { class: "deadlink", title: m[4] }, m[3] + " (" + m[4] + ")"));
    }
    last = re.lastIndex;
  }
  if (last < text.length) out.push(text.slice(last));
  return out;
}

function renderMarkdown(text, basePath) {
  const root = h("div", { class: "md" });
  const lines = text.replace(/\r/g, "").split("\n");
  const isBlock = (l) => /^(```|#{1,6}\s|\s*([-*]|\d+\.)\s|>|\|)/.test(l) || /^(-{3,}|\*{3,})\s*$/.test(l);
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (/^```/.test(line)) {
      const code = [];
      for (i++; i < lines.length && !/^```/.test(lines[i]); i++) code.push(lines[i]);
      i++;
      root.append(h("pre", {}, h("code", {}, code.join("\n"))));
    } else if (/^#{1,6}\s/.test(line)) {
      const m = line.match(/^(#{1,6})\s+(.*)$/);
      root.append(h("h" + Math.min(6, m[1].length + 1), { class: "mdh" }, inline(m[2], basePath)));
      i++;
    } else if (/^(-{3,}|\*{3,})\s*$/.test(line)) { root.append(h("hr")); i++; }
    else if (/^\|/.test(line) && /^\|?[\s:|-]+\|[\s:|-]*$/.test(lines[i + 1] || "")) {
      const cells = (l) => l.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
      const head = cells(line), body = [];
      for (i += 2; i < lines.length && /^\|/.test(lines[i]); i++) body.push(cells(lines[i]));
      root.append(h("div", { class: "tablewrap" }, h("table", {}, h("thead", {}, h("tr", {}, head.map((c) => h("th", {}, inline(c, basePath))))),
        h("tbody", {}, body.map((r) => h("tr", {}, r.map((c) => h("td", {}, inline(c, basePath)))))))));
    } else if (/^>/.test(line)) {
      const q = [];
      for (; i < lines.length && /^>/.test(lines[i]); i++) q.push(lines[i].replace(/^>\s?/, ""));
      root.append(h("blockquote", {}, inline(q.join(" "), basePath)));
    } else if (/^\s*([-*]|\d+\.)\s/.test(line)) {
      const ordered = /^\s*\d+\./.test(line), ul = h(ordered ? "ol" : "ul", { class: "mdlist" });
      for (; i < lines.length && /^\s*([-*]|\d+\.)\s/.test(lines[i]); i++) {
        const m = lines[i].match(/^(\s*)(?:[-*]|\d+\.)\s+(.*)$/);
        ul.append(h("li", { class: "ind" + Math.min(3, Math.floor(m[1].length / 2)) }, inline(m[2], basePath)));
      }
      root.append(ul);
    } else if (!line.trim()) i++;
    else {
      const p = [];
      for (; i < lines.length && lines[i].trim() && !isBlock(lines[i]); i++) p.push(lines[i].trim());
      if (!p.length) { p.push(lines[i].trim()); i++; }
      root.append(h("p", {}, inline(p.join(" "), basePath)));
    }
  }
  return root;
}

// What a repository document is, derived from the catalog only (never from the requested string).
function describeDoc(path) {
  const area = catalog.areas.find((a) => a.path && path.startsWith(a.path + "/"));
  const ex = catalog.exercises.find((e) => e.readme === path);
  const node = catalog.nodes.find((n) => n.content_path === path);
  const doc = (catalog.documents || []).find((d) => d.path === path);
  const phaseLabel = (a) => (a.phase ? a.phase + " — " : "") + a.name;
  if (ex) return { area: areaById[ex.area], kind: "Experiment", title: expLabel(ex) };
  if (area && path === area.path + "/README.md") return { area, kind: "Phase overview", title: phaseLabel(area) };
  if (node) return { area: areaById[node.area], kind: "Theory", title: node.name };
  if (doc) return { area: null, kind: "Document", title: doc.title };
  return { area: area || null, kind: "Document", title: path.split("/").pop() };
}

async function docView(path) {
  const backHref = modeHash();
  const goBack = () => { if (navCount > 0) history.back(); else location.hash = backHref; };
  let doc;
  try { doc = await api("/api/content?path=" + encodeURIComponent(path)); }
  catch (e) { return h("div", { class: "card" }, h("p", { class: "error" }, "Cannot open this file: " + e.message), h("a", { href: backHref }, "← back to the map")); }
  const info = describeDoc(path);
  const rendered = renderMarkdown(doc.text, path), raw = h("pre", { class: "rawdoc hidden" }, doc.text);
  const toggle = h("button", { type: "button", class: "secondary", onclick: () => {
    rendered.classList.toggle("hidden"); raw.classList.toggle("hidden");
    toggle.textContent = rendered.classList.contains("hidden") ? "Show rendered" : "Show raw Markdown"; } }, "Show raw Markdown");
  const crumbs = [h("a", { href: "#/" }, "Atlas")];
  if (info.area && info.area.path) crumbs.push(" › ", h("a", { href: "#/phase/" + info.area.id }, (info.area.phase ? info.area.phase + " — " : "") + info.area.name));
  crumbs.push(" › ", h("strong", {}, info.kind === "Experiment" ? info.title : info.kind === "Document" ? info.title : info.kind));
  return h("div", { class: "docview" },
    h("div", { class: "crumbs" }, h("button", { type: "button", class: "secondary", onclick: goBack }, "← Back"), h("span", {}, crumbs), h("span", { class: "spacer" }), toggle),
    h("p", { class: "muted source" }, "Source: ", h("code", {}, doc.path), " — read-only view; the repository file is the source of truth."),
    rendered, raw);
}

async function render() {
  const app = document.getElementById("app");
  const old = app.querySelector(".mapwrap");
  const keep = old ? [old.scrollLeft, old.scrollTop] : null;
  try {
    await load();
    const hash = location.hash || "#/";
    const nodeM = hash.match(/^#\/node\/([\w.-]+)$/), phaseM = hash.match(/^#\/phase\/([\w-]+)$/), docM = hash.match(/^#\/doc\/(.+)$/);
    const selected = nodeM && nodeById[nodeM[1]] ? nodeM[1] : null;
    if (hash === "#/" || hash === "#/atlas") mapMode = "overview";
    else if (hash === "#/detail" || hash === "#/map") mapMode = "detail";
    else if (phaseM && areaById[phaseM[1]]) mapMode = "phase:" + phaseM[1];
    else if (selected && mapMode === "overview") mapMode = "phase:" + nodeById[selected].area;
    const isMap = !!(hash === "#/" || hash === "#/atlas" || hash === "#/detail" || hash === "#/map" || (phaseM && areaById[phaseM[1]]) || selected);
    document.getElementById("nav-map").classList.toggle("active", isMap && mapMode !== "detail");
    document.getElementById("nav-detail").classList.toggle("active", isMap && mapMode === "detail");
    document.getElementById("nav-dashboard").classList.toggle("active", !isMap && !docM);
    if (docM) app.replaceChildren(await docView(decodeURIComponent(docM[1])));
    else app.replaceChildren(isMap ? mapView(selected, selected ? await nodePanel(selected) : null) : dashboard());
    fitMapHeight();
    const wrapEl = app.querySelector(".mapwrap");
    if (wrapEl) {
      if (keep) { wrapEl.scrollLeft = keep[0]; wrapEl.scrollTop = keep[1]; }
      else if (mapMode === "overview") { wrapEl.scrollLeft = 0; wrapEl.scrollTop = 0; } // whole route from the top; the current phase is in view
      else {
        const cur = wrapEl.querySelector(".node.current .box, .phase.current .box");
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

// The map viewport ends at the bottom of the window, so its horizontal scrollbar never hides below the fold.
function fitMapHeight() {
  const cols = document.querySelector(".mapcols");
  if (!cols) return;
  if (window.innerWidth <= 900) { cols.style.height = ""; return; }
  cols.style.height = Math.max(320, Math.floor(window.innerHeight - cols.getBoundingClientRect().top - 28)) + "px";
}
let resizeTimer;
window.addEventListener("resize", () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => { if (document.querySelector("svg.overview")) render(); else fitMapHeight(); }, 150);
});
let navCount = 0; // in-app hash navigations since load: lets Back stay inside the app
window.addEventListener("hashchange", () => { navCount++; });
window.addEventListener("hashchange", render);
window.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && /^#\/node\//.test(location.hash)) location.hash = modeHash(); });
render();
