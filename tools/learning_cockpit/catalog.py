"""Load and validate the versioned curriculum (catalog/catalog.json)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
CATALOG_PATH = HERE / "catalog" / "catalog.json"


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
    for area in catalog["areas"]:
        if "path" in area and resolve_repo_path(area["path"], root) is None:
            raise CatalogError(f"area {area['id']}: path does not exist: {area['path']}")
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
        if nid in node.get("prerequisites", []):
            raise CatalogError(f"node {nid}: lists itself as prerequisite")
        for res in node.get("resources", []):
            if "path" in res and resolve_repo_path(res["path"], root) is None:
                raise CatalogError(f"node {nid}: resource path does not exist: {res['path']}")
            if "path" not in res and "url" not in res:
                raise CatalogError(f"node {nid}: resource needs path or url")
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


def load_catalog(path=CATALOG_PATH, root=REPO_ROOT):
    with open(path, encoding="utf-8") as fh:
        return validate(json.load(fh), root)
