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

## The map

The landing view is a knowledge map drawn as SVG from `catalog.json`: one column per area in route order, rows follow each area's own prerequisite chain, and a later area is shifted down only as far as its cross-area prerequisites require (so Local Models & Inference starts right after Autoregressive Generation). Lines are prerequisites; dashed accent lines leave the current target. The map uses the full width; details open in a right-hand drawer (Esc or × closes it), and the initial scroll centres the current target. Nothing about the curriculum is hardcoded in the frontend. Each node shows its status with a label, a glyph and its border (dashed = pending, solid coloured = studying / practiced, filled green = validated); planned future areas are faded. Click a node to open its panel: description, prerequisites, what it leads to, exercises, repository resources, evidence, a status selector, an evidence form and "Set as current target". The Dashboard (secondary) keeps goal, counts, tasks and sessions.

Three independent things are shown on the map:

| Concept | Where it comes from | Shown as |
|---|---|---|
| **Completed through** (Experiment 29) | `completed_through` in the catalog, mirroring `ROADMAP.md`; a node counts as *lab path completed* when it has exercise folders | green bar on the node, green lines between covered nodes, top banner |
| **Current target** (Experiment 30 by default) | SQLite `plan.next_node_id`, else catalog `default_target` | **YOU ARE HERE** marker and glow, top banner |
| **Mastery** | SQLite `mastery` rows; no row = `pending` | glyph and border style |

Nodes on the completed lab path are deliberately *not* auto-rated: coverage is an overlay, no mastery rows are seeded, and an existing `progress.db` is never modified by it. Rate nodes yourself (`practiced` is the honest choice for exercises you have run; `validated` needs evidence). When the roadmap advances, update `completed_through` and `default_target` in the catalog.

**YOU ARE HERE** marks the *current learning target*. It is independent of mastery: a node can be the target while `pending`. It is read from the personal database (`plan.next_node_id`, set from a node panel or the dashboard). Until one is stored, the map uses `default_target` from the catalog (`llm.generation`), which mirrors `ROADMAP.md` (Experiment 29 complete, Experiment 30 next). That default is a single node id, not a copy of the roadmap, and nothing synchronizes the two: if the roadmap moves on, update `default_target` or set the target in the UI. The map is never validated visually by the tests; check it in a browser.

Area numbering follows the repository convention `topics/NN_*` = `ROADMAP.md` Phase NN. AI Automation & Agentic Systems is future curriculum (roadmap Phases 14–15); it has no topic directory yet.

## Sources of truth

```text
Repository Markdown (README.md, ROADMAP.md, docs/, topic READMEs) = canonical long-form learning content
ROADMAP.md                = versioned pedagogical route (the intended order)
catalog/catalog.json      = thin index: ids, one-line summaries, prerequisites, related nodes, paths
data/progress.db (SQLite) = mutable personal state: statuses, evidence, next step, tasks, sessions
```

The catalog does not hold theory; read the linked files for that. A node existing in the catalog says nothing about whether you have studied it. The "next step" field is a free operational note (optionally pointing at a node); it does not replace `ROADMAP.md`, and nothing synchronizes the two. The current position in the roadmap (Experiment 29 complete, Experiment 30 next) is stated in `ROADMAP.md`, not here.

## Three separate kinds of data

| Kind | Where | Versioned |
|---|---|---|
| **Curriculum** — areas, knowledge nodes, prerequisites, related topics, resources, the 29 exercise folders | `catalog/catalog.json` | yes |
| **Personal mastery** — status per node (`pending`, `studying`, `practiced`, `validated`) plus evidence | `data/progress.db` (SQLite) | **no** (`data/` is in `.gitignore`) |
| **Learning plan** — next step, pending tasks, session log, last activity | same database | **no** |

A node with no row is `pending`. `validated` requires at least one evidence entry. Evidence kinds are `exercise`, `test`, `evaluation`, `comment`, `file`; an optional reference must be an existing path inside the repository. A passing test is stored as evidence but never changes a status by itself: you decide.

An existing `progress.db` is opened, never replaced. A database written by a newer schema version is refused instead of modified. Back up progress by copying `data/progress.db`.

## Editing the curriculum

Edit `catalog/catalog.json`. It is validated on every start and in the tests: unique ids, known prerequisite/related/exercise references, no prerequisite cycles, and every referenced path must exist. Resources currently point only at files inside this repository; an entry may use `url` instead of `path`.

## Security notes

Loopback only; three fixed static files; no endpoint reads arbitrary paths or runs commands; POST requires `Content-Type: application/json`, rejects foreign `Origin`, and requests with a non-loopback `Host` header are refused. The UI renders all text with `textContent`.

## Limitations

- Single user, single process, no login.
- Node descriptions are short summaries written for the catalog; the exercise READMEs remain the source of truth.
- Map layout is automatic and basic (SVG, horizontal scroll if wide); `related` links appear in the panel, not as lines.
- Evidence cannot be edited or deleted from the UI yet.
- Tested only on Python 3.13.2, Windows 11.
- Exercises are **not executed** by the cockpit; the exercise `main.py` files need PyTorch, scikit-learn, etc., which are listed in the root `requirements.txt`.
- The external incident-triage experiment is not integrated, and its future location is undecided until the roadmap assigns the automation/agents phase.

## Possible later additions

Graph view, editing/removing evidence, import of external resources and courses, export of progress, integrating the triage experiment. Deliberately out of the MVP: accounts, cloud sync, AI API calls, generated courses, agents.
