"""Load and validate the versioned curriculum (catalog/catalog.json)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
CATALOG_PATH = HERE / "catalog" / "catalog.json"


TECH_TIERS = {"hands-on", "compare", "awareness", "enterprise-mapping"}
CONTENT_STATUSES = ("available", "partial", "implied", "planned")


class CatalogError(ValueError):
    pass


def resolve_repo_path(rel, root=REPO_ROOT):
    """Return an existing path inside the repo for a relative reference, else None."""
    if not isinstance(rel, str) or not rel or Path(rel).is_absolute() or "\\" in rel:
        return None
    root = Path(root).resolve()
    target = (root / rel).resolve()
    if target != root and root not in target.parents:
        return None
    return target if target.exists() else None


def content_paths(catalog):
    """Every repository Markdown file the Cockpit may serve read-only; nothing else is reachable."""
    paths = {d["path"] for d in catalog.get("documents", [])}
    for area in catalog["areas"]:
        if "path" in area:
            paths.add(area["path"] + "/README.md")
    paths.update(ex["readme"] for ex in catalog["exercises"])
    for node in catalog["nodes"]:
        if node.get("content_path"):
            paths.add(node["content_path"])
        paths.update(r["path"] for r in node.get("resources", []) if str(r.get("path", "")).endswith(".md"))
    return paths


def _unique(items, kind):
    ids = [item.get("id") for item in items]
    if len(ids) != len(set(ids)) or not all(isinstance(i, str) and i for i in ids):
        raise CatalogError(f"{kind} ids must be non-empty and unique")
    return set(ids)


def validate(catalog, root=REPO_ROOT):
    for key in ("goal", "areas", "nodes", "exercises"):
        if key not in catalog:
            raise CatalogError(f"missing key: {key}")
    area_ids = _unique(catalog["areas"], "area")
    node_ids = _unique(catalog["nodes"], "node")
    exercise_ids = _unique(catalog["exercises"], "exercise")
    track_ids = _unique(catalog.get("tracks", []), "track")
    _unique(catalog.get("resources", []), "resource")
    for area in catalog["areas"]:
        if "path" in area and resolve_repo_path(area["path"], root) is None:
            raise CatalogError(f"area {area['id']}: path does not exist: {area['path']}")
        if area.get("track") not in track_ids:
            raise CatalogError(f"area {area['id']}: unknown track")
    for ex in catalog["exercises"]:
        if ex.get("area") not in area_ids:
            raise CatalogError(f"exercise {ex['id']}: unknown area")
        for key in ("path", "entrypoint", "readme"):
            if resolve_repo_path(ex.get(key), root) is None:
                raise CatalogError(f"exercise {ex['id']}: {key} does not exist: {ex.get(key)}")
    for node in catalog["nodes"]:
        nid = node["id"]
        if node.get("area") not in area_ids:
            raise CatalogError(f"node {nid}: unknown area")
        for key, valid in (("prerequisites", node_ids), ("related", node_ids), ("exercises", exercise_ids)):
            for ref in node.get(key, []):
                if ref not in valid:
                    raise CatalogError(f"node {nid}: unknown {key} reference {ref}")
        if node.get("track", next(a for a in catalog["areas"] if a["id"] == node["area"])["track"]) not in track_ids:
            raise CatalogError(f"node {nid}: unknown track")
        if nid in node.get("prerequisites", []):
            raise CatalogError(f"node {nid}: lists itself as prerequisite")
        for res in node.get("resources", []):
            if "path" in res and resolve_repo_path(res["path"], root) is None:
                raise CatalogError(f"node {nid}: resource path does not exist: {res['path']}")
            if "path" not in res and "url" not in res:
                raise CatalogError(f"node {nid}: resource needs path or url")
    for node in catalog["nodes"]:
        nid, status, cpath = node["id"], node.get("content_status"), node.get("content_path")
        if status not in CONTENT_STATUSES:
            raise CatalogError(f"node {nid}: content_status must be one of {CONTENT_STATUSES}")
        if (status == "planned") == bool(cpath):
            raise CatalogError(f"node {nid}: content_path is required unless content_status is 'planned' (and forbidden then)")
        if cpath and (not cpath.endswith(".md") or resolve_repo_path(cpath, root) is None):
            raise CatalogError(f"node {nid}: content_path must be an existing repository .md file: {cpath}")
    for doc in catalog.get("documents", []):
        if not doc.get("title") or not str(doc.get("path", "")).endswith(".md") or resolve_repo_path(doc["path"], root) is None:
            raise CatalogError(f"document {doc.get('id')}: needs a title and an existing .md path")
    _unique(catalog.get("documents", []), "document")
    caps = _unique(catalog.get("capabilities", []), "capability")
    for cap in catalog.get("capabilities", []):
        if not cap.get("name") or not cap.get("nodes") or any(n not in node_ids for n in cap["nodes"]):
            raise CatalogError(f"capability {cap['id']}: needs a name and known node references")
    _unique(catalog.get("roles", []), "role")
    for role in catalog.get("roles", []):
        if any(c not in caps for c in role.get("capabilities", [])) or any(a not in area_ids for a in role.get("areas", [])):
            raise CatalogError(f"role {role['id']}: unknown capability or area")
    for res in catalog.get("resources", []):
        rid = res["id"]
        if not str(res.get("url", "")).startswith("https://") or not res.get("name"):
            raise CatalogError(f"resource {rid}: needs a name and an https url")
        if not res.get("nodes") or any(n not in node_ids for n in res["nodes"]):
            raise CatalogError(f"resource {rid}: needs known node references")
    for tech in catalog.get("technologies", []):
        tid = tech["id"]
        if tech.get("tier") not in TECH_TIERS or not tech.get("name"):
            raise CatalogError(f"technology {tid}: needs a name and a tier in {sorted(TECH_TIERS)}")
        if not tech.get("nodes") or any(n not in node_ids for n in tech["nodes"]):
            raise CatalogError(f"technology {tid}: needs known node references")
    _unique(catalog.get("technologies", []), "technology")
    if catalog.get("default_target") not in node_ids:
        raise CatalogError("default_target must be a known node")
    done = catalog.get("completed_through", {})
    if done.get("node") not in node_ids:
        raise CatalogError("completed_through.node must be a known node")
    _check_acyclic(catalog["nodes"])
    return catalog


def _check_acyclic(nodes):
    prereqs = {n["id"]: n.get("prerequisites", []) for n in nodes}
    state = {}

    def visit(nid):
        if state.get(nid) == 1:
            raise CatalogError(f"prerequisite cycle through {nid}")
        if state.get(nid) == 2:
            return
        state[nid] = 1
        for p in prereqs[nid]:
            visit(p)
        state[nid] = 2

    for nid in prereqs:
        visit(nid)


def _section(text, heading):
    """First paragraph under '## heading' in a Markdown string, whitespace-collapsed ('' if absent)."""
    lines, out, on = text.splitlines(), [], False
    for line in lines:
        if on and (line.startswith("#") or (out and not line.strip())):
            break
        if on and line.strip():
            out.append(line.strip())
        elif line.strip().lower() == "## " + heading.lower():
            on = True
    return " ".join(out)


def enrich(catalog, root=REPO_ROOT):
    """Derive presentation metadata from canonical sources; nothing here is stored a second time.

    - exercise["number"]: global Experiment NN = position in the ordered exercises list.
    - area["purpose"] / area["why"]: the phase README's "Purpose" / "Why it matters" sections,
      unless the catalog states them explicitly (phases whose README predates that template).
    """
    for number, ex in enumerate(catalog["exercises"], start=1):
        ex["number"] = number
    for area in catalog["areas"]:
        readme = resolve_repo_path(area["path"] + "/README.md", root) if "path" in area else None
        text = readme.read_text(encoding="utf-8") if readme else ""
        area.setdefault("purpose", _section(text, "Purpose") or area["description"])
        why = _section(text, "Why it matters")
        if why:
            area.setdefault("why", why)
    return catalog


def load_catalog(path=CATALOG_PATH, root=REPO_ROOT):
    with open(path, encoding="utf-8") as fh:
        return enrich(validate(json.load(fh), root), root)
