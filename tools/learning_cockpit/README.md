# Learning Cockpit

A small local web app that shows the repository's knowledge map, links each topic to the real exercise folders, and stores **your own** progress. MVP; Python standard library only (no install step, no network, no paid service).

## Run

From the repository root:

```bash
python tools/learning_cockpit/app.py            # http://127.0.0.1:8765/
python tools/learning_cockpit/app.py --port 9000
python tools/learning_cockpit/app.py --data-dir path/to/dir
```

The server refuses any host other than `127.0.0.1`, `localhost` or `::1`.

## Test

Validated with the repository interpreter `.venv\Scripts\python.exe` (Python 3.13). Windows example:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tools/learning_cockpit/tests -v
```

Generic form:

```bash
python -m unittest discover -s tools/learning_cockpit/tests -v
```

## The atlas

The Cockpit is a local knowledge atlas over the curriculum. The flow is:

```text
Overview (17 phases, two tracks)  →  click a phase  →  its concepts (+ neighbouring phases, faded)
→  click a concept  →  drawer: what it is · why it matters · where you are · prerequisites · theory · experiments · mastery · evidence
```

- **Overview** (`#/`): one box per phase, columns Core | Bridge | Applied, rows from the prerequisites between phases, plus the Cross-cutting strip. `TRACK A STARTS`, `TRACK B STARTS` and `TRACKS CONVERGE` are derived from the catalog. Each card shows phase number, name, track, state (lab path completed / in progress / planned), a one-line purpose, concept and experiment counts and theory availability, plus the lab-path bar; `YOU ARE HERE` marks the phase of the current target. The drawing fills the available width and is scaled to the window height (never below 90%).
- **Phase view** (`#/phase/<area>`): an orientation header (what this phase is, why it matters, what you will learn, where it fits, status, **Open phase overview**), then that phase's concepts plus the concepts they depend on or lead to in other phases (faded). Purpose and "why it matters" are read from the phase README's `## Purpose` and `## Why it matters` sections (catalog `purpose` / `why` override them for Phases 01–04, whose READMEs predate that template); prerequisites and neighbours come from the concept graph.
- **Detailed map** (`#/detail`): every concept at once. The map viewport is fitted to the window, so its horizontal scrollbar is always on screen (Shift+wheel and trackpads also work). "What do these mean?" in the legend defines mastery, lab path completed, current target, needed next and planned.
- **Theory viewer** (`#/doc/<path>`): a breadcrumb (Atlas › Phase › Theory / Experiment), the repository path as a secondary "Source" line, and a modest, read-only Markdown view (headings, lists, code, tables, links; a raw toggle). The source stays the repository file. `GET /api/content?path=` serves **only** Markdown files the catalog itself references (`content_path`, exercise READMEs, phase READMEs, `documents`); anything else, including traversal, absolute paths, non-Markdown files and the database, returns 404.
- **Theory status** per concept: `available` (a canonical file explains it), `partial`, `implied` (only implied by an experiment) or `planned` (honestly not written yet; shown as "Theory: planned"). Future theory is written when its phase begins, not generated in advance.

### Experiment numbers

The UI shows the **global** Experiment NN (position in the catalog's ordered `exercises` list, derived in `catalog.py`, not stored). Repository folders keep their historical local numbers (`topics/04_llm_engineering/02_embeddings` is Experiment 14). See [learning method](../../docs/learning-method.md#experiment-numbering).

### The map details

The Detailed and Phase maps are knowledge maps drawn as SVG from `catalog.json`: one column per area in route order, rows follow each area's own prerequisite chain, and a later area is shifted down only as far as its cross-area prerequisites require (so Local Models & Inference starts right after Autoregressive Generation). Lines are prerequisites; dashed accent lines leave the current target. The map uses the full width; details open in a right-hand drawer (Esc or × closes it), and the initial scroll centres the current target. Nothing about the curriculum is hardcoded in the frontend. Each node shows its status with a label, a glyph and its border (dashed = pending, solid coloured = studying / practiced, filled green = validated); planned future areas are faded. Click a node to open its panel: description, prerequisites, what it leads to, exercises, repository resources, evidence, a status selector, an evidence form and "Set as current target". The Dashboard (secondary) keeps goal, counts, tasks and sessions.

Three independent things are shown on the map:

| Concept | Where it comes from | Shown as |
|---|---|---|
| **Completed through** (Experiment 29) | `completed_through` in the catalog, mirroring `ROADMAP.md`; a node counts as *lab path completed* when it has exercise folders | green bar on the node, green lines between covered nodes, top banner |
| **Current target** (Experiment 30 by default) | SQLite `plan.next_node_id`, else catalog `default_target` | **YOU ARE HERE** marker and glow, top banner |
| **Mastery** | SQLite `mastery` rows; no row = `pending` | glyph and border style |

Nodes on the completed lab path are deliberately *not* auto-rated: coverage is an overlay, no mastery rows are seeded, and an existing `progress.db` is never modified by it. Rate nodes yourself (`practiced` is the honest choice for exercises you have run; `validated` needs evidence). When the roadmap advances, update `completed_through` and `default_target` in the catalog.

**YOU ARE HERE** marks the *current learning target*. It is independent of mastery: a node can be the target while `pending`. It is read from the personal database (`plan.next_node_id`, set from a node panel or the dashboard). Until one is stored, the map uses `default_target` from the catalog (`llm.generation`), which mirrors `ROADMAP.md` (Experiment 29 complete, Experiment 30 next). That default is a single node id, not a copy of the roadmap, and nothing synchronizes the two: if the roadmap moves on, update `default_target` or set the target in the UI. The map is never validated visually by the tests; check it in a browser.

Area numbering follows the repository convention `topics/NN_*` = `ROADMAP.md` Phase NN. Every phase 01–17 is its own area; Phases 05–17 are planned areas with README-only topic directories. Only the "Cross-cutting Skills" lane has no topic directory. Concept ids such as `later.backend` predate the split of the old grouped lane into Phases 13–17 and are kept unchanged because ids are the keys of your personal progress.

Each area and node carries a learning **track** (`core`, `applied`, `bridge`, `cross-cutting`, defined in the catalog `tracks` list); lanes are tinted by track and the node drawer states it. Concepts are nodes; technologies are not. A top-level `technologies` registry (id, name, `tier` = `hands-on` / `compare` / `awareness` / `enterprise-mapping`, mapped `nodes`, purpose) lists products without creating a node each; it is validated and shown in the node drawer. External courses live in one catalog registry, `resources` (id, name, type, provider, url, cost, mapped `nodes`, `timing`), and appear in the drawer of every mapped node as plain links; nothing is fetched or tracked.

## Sources of truth

```text
Repository Markdown (README.md, ROADMAP.md, docs/, topic READMEs) = canonical long-form learning content
ROADMAP.md                = versioned pedagogical route (the intended order)
catalog/catalog.json      = thin index: ids, one-line summaries, prerequisites, related nodes, paths,
                            one canonical `content_path` per concept, documents / capabilities / roles / technologies registries
data/progress.db (SQLite) = mutable personal state: statuses, evidence, next step, tasks, sessions
```

The catalog does not hold theory; read the linked files for that. A node existing in the catalog says nothing about whether you have studied it. The "next step" field is a free operational note (optionally pointing at a node); it does not replace `ROADMAP.md`, and nothing synchronizes the two. The current position in the roadmap (Experiment 29 complete, Experiment 30 next) is stated in `ROADMAP.md`, not here.

## Three separate kinds of data

| Kind | Where | Versioned |
|---|---|---|
| **Curriculum** — areas, knowledge nodes, prerequisites, related topics, resources, the 29 exercise folders | `catalog/catalog.json` | yes |
| **Personal mastery** — status per node (`pending`, `studying`, `practiced`, `validated`) plus evidence | `data/progress.db` (SQLite) | **no** (`data/` is in `.gitignore`) |
| **Learning plan** — next step, pending tasks, session log, last activity | same database | **no** |

A node with no row is `pending`. `validated` requires at least one evidence entry. Evidence kinds (served by the backend, not copied into the frontend) are `exercise`, `test`, `evaluation`, `comment`, `file`; an optional reference must be an existing path inside the repository. A passing test is stored as evidence but never changes a status by itself: you decide.

An existing `progress.db` is opened, never replaced. A database written by a newer schema version is refused instead of modified. Back up progress by copying `data/progress.db`.

## Editing the curriculum

Edit `catalog/catalog.json`. It is validated on every start and in the tests: unique ids, known prerequisite/related/exercise references, no prerequisite cycles, and every referenced path must exist. Each node carries `content_status` (`available` / `partial` / `implied` / `planned`) and, unless planned, one `content_path` to an existing repository `.md` file; capabilities, roles, documents and technologies are registries that reference node ids (roles and capabilities are curriculum targets, not job readiness). Per-node `resources` are only for extra repository files that are not derivable from the phase; the phase overview and roadmap links are derived. Per-node `resources` point at files inside this repository; external courses belong only in the top-level `resources` registry (https URLs, known node ids).

## Security notes

Loopback only; three fixed static files; the only file-reading endpoint is `/api/content`, an exact allowlist of catalog-referenced `.md` paths (read-only, no browsing); nothing runs commands; POST requires `Content-Type: application/json`, rejects foreign `Origin`, and requests with a non-loopback `Host` header are refused. The UI renders all text with `textContent`.

## Limitations

- Single user, single process, no login.
- Node descriptions are short summaries written for the catalog; the exercise READMEs remain the source of truth.
- Map layout is automatic and basic (SVG, scroll if wide); `related` links appear in the panel, not as lines. The Markdown viewer is deliberately small (no images, no nested-list structure, no in-page anchors).
- Evidence cannot be edited or deleted from the UI yet.
- Tested only on Python 3.13.2, Windows 11.
- Exercises are **not executed** by the cockpit; the exercise `main.py` files need PyTorch, scikit-learn, etc., which are listed in the root `requirements.txt`.
- The external incident-triage experiment is not integrated, and it may eventually become the first experiment of Phase 07 (AI Automation Foundations) and has not been moved.

## Possible later additions

Graph view, editing/removing evidence, import of external resources and courses, export of progress, integrating the triage experiment. Deliberately out of the MVP: accounts, cloud sync, AI API calls, generated courses, agents.
