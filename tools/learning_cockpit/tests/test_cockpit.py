import copy
import http.client
import json
import sys
import tempfile
import threading
import unittest
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_server  # noqa: E402
from catalog import CATALOG_PATH, CONTENT_STATUSES, REPO_ROOT, CatalogError, content_paths, load_catalog, validate  # noqa: E402
from store import EVIDENCE_KINDS, Store, ValidationError  # noqa: E402


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog()

    def test_loads_and_has_real_exercises(self):
        llm = [e for e in self.catalog["exercises"] if e["area"] == "llm"]
        self.assertEqual(len(llm), 17)
        on_disk = sorted(p.name for p in (REPO_ROOT / "topics/04_llm_engineering").iterdir() if p.is_dir())
        self.assertEqual(sorted(e["path"].split("/")[-1] for e in llm), on_disk)

    def test_every_topic_exercise_dir_is_cataloged(self):
        on_disk = {f"topics/{t.name}/{p.name}" for t in (REPO_ROOT / "topics").iterdir() if t.is_dir()
                   for p in t.iterdir() if p.is_dir() and p.name[:2].isdigit()}
        self.assertEqual(on_disk, {e["path"] for e in self.catalog["exercises"]})

    def test_ids_unique_and_paths_exist(self):
        for key in ("areas", "nodes", "exercises"):
            ids = [i["id"] for i in self.catalog[key]]
            self.assertEqual(len(ids), len(set(ids)), key)
        for ex in self.catalog["exercises"]:
            for k in ("path", "entrypoint", "readme"):
                self.assertTrue((REPO_ROOT / ex[k]).exists(), ex[k])

    def test_every_exercise_belongs_to_a_node(self):
        used = {e for n in self.catalog["nodes"] for e in n["exercises"]}
        self.assertEqual(used, {e["id"] for e in self.catalog["exercises"]})

    def test_invalid_catalogs_rejected(self):
        def broken(mutate):
            c = copy.deepcopy(self.catalog)
            mutate(c)
            with self.assertRaises(CatalogError):
                validate(c)
        broken(lambda c: c["nodes"].append(dict(c["nodes"][0])))                       # duplicate id
        broken(lambda c: c["nodes"][0]["prerequisites"].append("nope"))                # unknown prereq
        broken(lambda c: c["nodes"][0]["related"].append("nope"))                      # unknown related
        broken(lambda c: c["nodes"][0]["exercises"].append("nope"))                    # unknown exercise
        broken(lambda c: c["nodes"][0]["resources"].append({"title": "x", "path": "missing.md"}))
        broken(lambda c: c["nodes"][0]["resources"].append({"title": "x", "path": "../outside"}))
        broken(lambda c: c["exercises"][0].update(path="topics/nope"))
        broken(lambda c: c["nodes"][0]["prerequisites"].append(c["nodes"][0]["id"]))   # self prereq

        def cycle(c):
            a, b = c["nodes"][0], c["nodes"][1]
            a["prerequisites"] = [b["id"]]
            b["prerequisites"] = [a["id"]]
        broken(cycle)


class MapAndTopicAlignmentTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog()
        self.nodes = {n["id"]: n for n in self.catalog["nodes"]}

    def test_topic_numbers_match_area_phases(self):
        for area in self.catalog["areas"]:
            if "path" in area:
                self.assertEqual("Phase " + area["path"].split("/")[1][:2], area["phase"])
        self.assertEqual(self.catalog["areas"][4]["path"], "topics/05_local_models_inference")
        self.assertTrue((REPO_ROOT / "topics/05_local_models_inference/README.md").is_file())
        self.assertFalse((REPO_ROOT / "topics/05_ai_automation_agents").exists())
        self.assertNotIn("05_ai_automation_agents", CATALOG_PATH.read_text(encoding="utf-8"))
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("# Phase 05 — Local Models and Inference", roadmap)

    def test_future_phases_are_readme_only_planned_topics(self):
        expected = {"iface": "06_llm_application_interfaces", "automation": "07_ai_automation_foundations",
                    "retrieval": "08_embeddings_semantic_retrieval", "rag": "09_rag_knowledge_systems",
                    "agents": "10_agentic_systems", "mcp": "11_mcp_integration",
                    "frameworks": "12_agent_frameworks_orchestration"}
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        for area_id, directory in expected.items():
            area = next(a for a in self.catalog["areas"] if a["id"] == area_id)
            self.assertEqual(area["path"], "topics/" + directory)
            self.assertTrue(area["planned"])
            folder = REPO_ROOT / area["path"]
            self.assertEqual([p.name for p in folder.iterdir()], ["README.md"])  # no experiments, no code
            self.assertIn("PLANNED", (folder / "README.md").read_text(encoding="utf-8"))
            self.assertIn(f"# {area['phase']} — ", roadmap)
            nodes = [n for n in self.catalog["nodes"] if n["area"] == area_id]
            self.assertTrue(nodes and all(n["planned"] and not n["exercises"] for n in nodes), area_id)
        self.assertNotIn("path", next(a for a in self.catalog["areas"] if a["id"] == "cross"))  # visual grouping only
        self.assertNotIn("later", {a["id"] for a in self.catalog["areas"]})  # phases 13-17 are individual areas
        for directory in ("13_multimodal_voice", "14_model_adaptation", "15_ai_backend_client_integration",
                          "16_packaging_offline_distribution", "17_production_ai_engineering"):
            folder = REPO_ROOT / "topics" / directory
            self.assertEqual([p.name for p in folder.iterdir()], ["README.md"])
            self.assertIn("PLANNED", (folder / "README.md").read_text(encoding="utf-8"))
            self.assertIn(f"# Phase {directory[:2]} — ", roadmap)
        numbers = sorted(p.name[:2] for p in (REPO_ROOT / "topics").iterdir() if p.is_dir())
        self.assertEqual(numbers, [f"{i:02d}" for i in range(1, 18)])

    def test_tracks_cover_core_applied_bridge_and_cross_cutting(self):
        self.assertEqual({t["id"] for t in self.catalog["tracks"]}, {"core", "applied", "bridge", "cross-cutting"})
        used = {n.get("track") or next(a for a in self.catalog["areas"] if a["id"] == n["area"])["track"]
                for n in self.catalog["nodes"]}
        self.assertEqual(used, {"core", "applied", "bridge", "cross-cutting"})
        for nid in ("llm.training_loop", "local.inference"):  # Core path is preserved
            self.assertIn(self.nodes[nid]["track"], ("core", "bridge"))
        applied = {n["id"] for n in self.catalog["nodes"] if n.get("track") == "applied"}
        self.assertTrue({"auto.n8n", "agent.loop", "mcp.architecture", "fw.langgraph"} <= applied)

    def test_frameworks_come_after_fundamentals(self):
        def ancestors(nid, seen=None):
            seen = set() if seen is None else seen
            for p in self.nodes[nid]["prerequisites"]:
                if p not in seen:
                    seen.add(p)
                    ancestors(p, seen)
            return seen
        self.assertIn("agent.loop", ancestors("fw.langchain"))
        self.assertIn("agent.loop", ancestors("fw.langgraph"))
        self.assertIn("auto.reliability", ancestors("fw.n8n_ai"))
        self.assertIn("agent.loop", ancestors("mcp.architecture"))
        self.assertIn("iface.tool_calling", ancestors("agent.loop"))
        self.assertIn("rag.pipeline", ancestors("fw.langchain"))

    def test_resource_registry_maps_courses_to_nodes(self):
        resources = {r["id"]: r for r in self.catalog["resources"]}
        self.assertEqual(set(resources), {"hf-llm-course", "hf-agents-course", "langchain-learn", "n8n-learning"})
        for res in resources.values():
            self.assertTrue(res["url"].startswith("https://"))
            self.assertTrue(all(n in self.nodes for n in res["nodes"]))
            self.assertEqual(res["cost"], "free")
        self.assertIn("agent.loop", resources["hf-agents-course"]["nodes"])
        self.assertIn("auto.n8n", resources["n8n-learning"]["nodes"])
        # one canonical registry: URLs live in the catalog, not on individual nodes
        urls = {r["url"] for r in resources.values()}
        for n in self.catalog["nodes"]:
            self.assertFalse(urls & {r.get("url") for r in n["resources"]}, n["id"])

    def test_invalid_resources_and_tracks_rejected(self):
        def broken(mutate):
            c = copy.deepcopy(self.catalog)
            mutate(c)
            with self.assertRaises(CatalogError):
                validate(c)
        broken(lambda c: c["resources"].append(dict(c["resources"][0])))                       # duplicate id
        broken(lambda c: c["resources"][0].update(nodes=["nope"]))                              # unknown node
        broken(lambda c: c["resources"][0].update(url="http://insecure.example"))
        broken(lambda c: c["areas"][0].update(track="nope"))
        broken(lambda c: c["nodes"][0].update(track="nope"))

    def test_default_target_matches_roadmap_next(self):
        self.assertEqual(self.catalog["default_target"], "llm.generation")
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertRegex(roadmap, r"\| 30 \| Autoregressive Generation and Sampling \|[^\n]*\| \*\*NEXT")

    def test_completed_through_overlay_is_consistent(self):
        done = self.catalog["completed_through"]
        self.assertEqual(done["node"], "llm.training_loop")
        covered = {n["id"] for n in self.catalog["nodes"] if n["exercises"]}  # same rule as the UI
        self.assertIn(done["node"], covered)
        self.assertNotIn(self.catalog["default_target"], covered)  # target is not yet covered
        for nid in covered:  # covered set is closed under prerequisites
            self.assertTrue(set(self.nodes[nid]["prerequisites"]) <= covered, nid)
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertRegex(roadmap, r"\| 29 \| Language-Model Training Loop \|[^\n]*\| COMPLETE \|")
        bad = copy.deepcopy(self.catalog)
        bad["completed_through"]["node"] = "nope"
        with self.assertRaises(CatalogError):
            validate(bad)

    def test_map_edges_reference_known_nodes_across_areas(self):
        edges = [(p, n["id"]) for n in self.catalog["nodes"] for p in n["prerequisites"]]
        self.assertTrue(all(p in self.nodes for p, _ in edges))
        cross = {(self.nodes[p]["area"], self.nodes[n]["area"]) for p, n in edges if self.nodes[p]["area"] != self.nodes[n]["area"]}
        self.assertIn(("llm", "local"), cross)
        self.assertIn(("local", "iface"), cross)
        self.assertIn(("iface", "automation"), cross)  # applied track branches off the interfaces
        self.assertIn(("iface", "agents"), cross)
        self.assertIn(("rag", "frameworks"), cross)


class CurriculumExpansionTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog()
        self.nodes = {n["id"]: n for n in self.catalog["nodes"]}
        self.techs = {t["id"]: t for t in self.catalog["technologies"]}

    def test_position_and_phase_structure_unchanged(self):
        self.assertEqual(self.catalog["default_target"], "llm.generation")
        self.assertEqual(self.catalog["completed_through"]["node"], "llm.training_loop")
        self.assertEqual(len(self.catalog["exercises"]), 29)
        self.assertEqual(len(self.catalog["areas"]), 18)  # 17 phases + cross-cutting; no phase added

    def test_new_concepts_exist_and_are_planned_without_exercises(self):
        required = ["local.performance", "local.serving", "iface.prompt_contracts", "iface.prompt_evaluation",
                    "auto.api_integration", "auto.browser_automation", "ret.lexical_sparse", "ret.vector_indexes",
                    "rag.security", "agent.patterns", "agent.long_running", "mcp.a2a", "fw.microsoft_agent_framework",
                    "fw.copilot_studio", "later.event_driven", "later.containers", "later.llmops",
                    "later.prompt_optimization", "xc.delivery_outcomes"]
        for nid in required:
            self.assertTrue(self.nodes[nid]["planned"] and not self.nodes[nid]["exercises"], nid)

    def test_technology_registry_is_tiered_and_bounded(self):
        tiers = {t["tier"] for t in self.techs.values()}
        self.assertEqual(tiers, {"hands-on", "compare", "awareness", "enterprise-mapping"})
        self.assertLess(len(self.catalog["nodes"]), 110)  # concepts, not one node per product
        for name in ("crewai", "ag-ui", "vllm", "litellm", "autogen-semantic-kernel", "a2a", "dspy"):
            self.assertIn(self.techs[name]["tier"], ("awareness", "compare"), name)
        for name in ("langgraph", "microsoft-agent-framework", "ollama", "llama-cpp", "n8n", "mcp", "fastapi"):
            self.assertEqual(self.techs[name]["tier"], "hands-on", name)
        for name in ("azure-openai", "azure-ai-search", "copilot-studio", "microsoft-foundry"):
            self.assertEqual(self.techs[name]["tier"], "enterprise-mapping", name)

    def test_ordering_constraints(self):
        def anc(nid, seen=None):
            seen = set() if seen is None else seen
            for p in self.nodes[nid]["prerequisites"]:
                if p not in seen:
                    seen.add(p)
                    anc(p, seen)
            return seen
        self.assertIn("iface.prompt_evaluation", anc("later.prompt_optimization"))  # DSPy after manual evals
        self.assertIn("agent.loop", anc("fw.microsoft_agent_framework"))
        self.assertIn("mcp.architecture", anc("mcp.a2a"))
        self.assertIn("auto.api_integration", anc("auto.browser_automation"))  # API before browser
        self.assertIn("ret.similarity_search", anc("ret.lexical_sparse"))

    def test_invalid_technologies_rejected(self):
        for mutate in (lambda c: c["technologies"][0].update(tier="nope"),
                       lambda c: c["technologies"][0].update(nodes=["nope"]),
                       lambda c: c["technologies"].append(dict(c["technologies"][0]))):
            c = copy.deepcopy(self.catalog)
            mutate(c)
            with self.assertRaises(CatalogError):
                validate(c)

    def test_docs_state_the_new_rules(self):
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        for text in ("Professional competency layer", "Incremental delivery", "Outcome-oriented engineering",
                     "Agent2Agent", "Microsoft Agent Framework", "DSPy", "prefer supported APIs", "vLLM", "LiteLLM"):
            self.assertIn(text, roadmap)
        self.assertTrue((REPO_ROOT / "docs/professional-capabilities.md").is_file())
        method = (REPO_ROOT / "docs/learning-method.md").read_text(encoding="utf-8")
        self.assertIn("Incremental delivery", method)


class AtlasTests(unittest.TestCase):
    """Knowledge-atlas architecture: one canonical content link per concept, a safe read-only viewer, phase graph."""

    def setUp(self):
        self.catalog = load_catalog()
        self.nodes = {n["id"]: n for n in self.catalog["nodes"]}

    def broken(self, mutate):
        c = copy.deepcopy(self.catalog)
        mutate(c)
        with self.assertRaises(CatalogError):
            validate(c)

    def test_every_node_has_honest_content_metadata(self):
        for n in self.catalog["nodes"]:
            self.assertIn(n["content_status"], CONTENT_STATUSES, n["id"])
            if n["content_status"] == "planned":
                self.assertNotIn("content_path", n, n["id"])  # never pretend theory exists
            else:
                self.assertTrue(n["content_path"].endswith(".md") and (REPO_ROOT / n["content_path"]).is_file(), n["id"])
        for n in self.catalog["nodes"]:  # an experiment node's theory is its own experiment README
            if n["exercises"]:
                readmes = {e["readme"] for e in self.catalog["exercises"] if e["id"] in n["exercises"]}
                self.assertEqual((n["content_status"], n["content_path"] in readmes), ("available", True), n["id"])
        self.assertEqual(self.nodes["llm.generation"]["content_status"], "partial")  # Experiment 30 has no theory yet

    def test_invalid_content_metadata_rejected(self):
        self.broken(lambda c: c["nodes"][0].update(content_status="nope"))
        self.broken(lambda c: c["nodes"][0].pop("content_status"))
        self.broken(lambda c: c["nodes"][0].update(content_path="missing.md"))
        self.broken(lambda c: c["nodes"][0].update(content_path="../outside.md"))
        self.broken(lambda c: c["nodes"][0].update(content_path="tools/learning_cockpit/app.py"))  # not Markdown
        self.broken(lambda c: next(n for n in c["nodes"] if n["content_status"] == "planned").update(content_path="README.md"))
        self.broken(lambda c: c["nodes"][0].pop("content_path"))  # non-planned needs a path

    def test_phase_structure_and_overview_graph(self):
        phases = [a for a in self.catalog["areas"] if "path" in a]
        self.assertEqual([a["phase"] for a in phases], [f"Phase {i:02d}" for i in range(1, 18)])
        for a in phases:
            self.assertTrue(any(n["area"] == a["id"] for n in self.catalog["nodes"]), a["id"])
        graph = {a["id"]: set() for a in phases}
        for n in self.catalog["nodes"]:
            for p in n["prerequisites"]:
                if self.nodes[p]["area"] != n["area"] and n["area"] in graph and self.nodes[p]["area"] in graph:
                    graph[n["area"]].add(self.nodes[p]["area"])
        state = {}

        def visit(a):  # the Overview is derived from this graph; it must be acyclic
            self.assertNotEqual(state.get(a), 1, f"phase cycle through {a}")
            if state.get(a) == 2:
                return
            state[a] = 1
            for p in graph[a]:
                visit(p)
            state[a] = 2
        for a in graph:
            visit(a)
        connected = {a for a, ps in graph.items() if ps} | {p for ps in graph.values() for p in ps}
        self.assertEqual(connected, set(graph))  # every phase is reachable in the overview
        self.assertEqual({a["track"] for a in phases}, {"core", "applied", "bridge"})

    def test_core_chain_is_connected_across_phases(self):
        def anc(nid, seen=None):
            seen = set() if seen is None else seen
            for p in self.nodes[nid]["prerequisites"]:
                if p not in seen:
                    seen.add(p)
                    anc(p, seen)
            return seen
        self.assertIn("ml.supervised_classification", anc("llm.tokenization"))  # ML -> DL -> LLM, not a detached root
        self.assertIn("cv.mnist_cnn", anc("later.multimodal_voice"))
        roots = [n["id"] for n in self.catalog["nodes"] if not n["prerequisites"]]
        self.assertEqual(sorted(roots), ["auto.process_decomposition", "ml.supervised_classification", "xc.problem_framing"])

    def test_capabilities_roles_and_documents(self):
        caps = {c["id"]: c for c in self.catalog["capabilities"]}
        self.assertTrue({"tool_integration", "orchestration", "prompt_engineering", "mcp", "observability", "ai_security",
                         "solution_architecture", "event_driven", "cicd", "containers"} <= set(caps))
        roles = {r["id"]: r for r in self.catalog["roles"]}
        self.assertEqual(len(roles), 8)
        for r in roles.values():
            reached = {n for c in r["capabilities"] for n in caps[c]["nodes"]} | {n["id"] for n in self.catalog["nodes"] if n["area"] in r["areas"]}
            self.assertTrue(reached, r["id"])
        self.broken(lambda c: c["capabilities"][0].update(nodes=["nope"]))
        self.broken(lambda c: c["roles"][0]["capabilities"].append("nope"))
        self.broken(lambda c: c["roles"][0]["areas"].append("nope"))
        self.broken(lambda c: c["documents"].append({"id": "x", "title": "x", "path": "nope.md", "role": ""}))
        for d in self.catalog["documents"]:
            self.assertTrue((REPO_ROOT / d["path"]).is_file(), d["path"])

    def test_no_generic_resource_duplication_and_no_orphans(self):
        for n in self.catalog["nodes"]:  # phase overview / roadmap links are derived from the area, not repeated per node
            self.assertFalse([r for r in n["resources"] if r.get("title") in ("Phase overview", "Roadmap")], n["id"])
            self.assertNotIn("docs/learning-method.md", [r.get("path") for r in n["resources"]], n["id"])
            linked = n["prerequisites"] or n["related"] or any(n["id"] in m["prerequisites"] or n["id"] in m["related"] for m in self.catalog["nodes"])
            self.assertTrue(linked, f"orphan {n['id']}")

    def test_frontend_has_no_hardcoded_content_paths(self):
        import re
        js = (Path(__file__).resolve().parent.parent / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"(topics|docs|tools)/[\w.-]+", js))
        self.assertIsNone(re.search(r"\bKINDS\b", js))  # evidence kinds come from the server, not a copy


class OrientationTests(unittest.TestCase):
    """Presentation metadata is derived from canonical sources, not stored a second time."""

    def setUp(self):
        self.catalog = load_catalog()

    def test_global_experiment_numbers_follow_catalog_order(self):
        self.assertEqual([e["number"] for e in self.catalog["exercises"]], list(range(1, 30)))
        by_id = {e["id"]: e for e in self.catalog["exercises"]}
        self.assertEqual(by_id["ex-llm-01_tokenization"]["number"], 13)   # roadmap: Experiment 13
        self.assertEqual(by_id["ex-llm-17_training_loop"]["number"], 29)  # roadmap: Experiment 29

    def test_roadmap_experiment_table_matches_catalog(self):
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        for ex in self.catalog["exercises"]:
            if ex["area"] == "llm":
                folder = ex["path"].split("/")[-1]
                self.assertRegex(roadmap, rf"\| {ex['number']} \|[^\n]*\| `{folder}` \| COMPLETE \|")

    def test_every_phase_has_purpose_and_why(self):
        for area in self.catalog["areas"]:
            if "path" in area:
                self.assertTrue(area["purpose"], area["id"])
                self.assertTrue(area.get("why"), area["id"])
        local = next(a for a in self.catalog["areas"] if a["id"] == "local")
        self.assertIn("locally", local["purpose"])  # taken from topics/05_*/README.md, not stored twice

    def test_frontend_stays_text_only_and_back_stays_in_app(self):
        js = (Path(__file__).resolve().parent.parent / "static" / "app.js").read_text(encoding="utf-8")
        self.assertIn("function describeDoc", js)
        self.assertIn("navCount", js)
        self.assertNotRegex(js, r"\.(innerHTML|outerHTML)\s*=|insertAdjacentHTML")


class ContentEndpointTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.server = create_server("127.0.0.1", 0, self.tmp.name)
        self.port = self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.catalog = load_catalog()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.server.store.close()
        self.tmp.cleanup()

    def call(self, method, path, host=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        headers = {"Host": host} if host else {}
        body = None
        if method == "POST":
            headers["Content-Type"] = "application/json"
            body = "{}"
        conn.request(method, path, body, headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()
        return res.status, data

    def test_serves_catalog_approved_markdown_read_only(self):
        for path in ("topics/04_llm_engineering/17_training_loop/README.md", "ROADMAP.md", "docs/learning-method.md",
                     "topics/05_local_models_inference/README.md"):
            status, body = self.call("GET", "/api/content?path=" + urllib.parse.quote(path))
            self.assertEqual(status, 200, path)
            doc = json.loads(body)
            self.assertEqual((doc["path"], doc["text"]), (path, (REPO_ROOT / path).read_text(encoding="utf-8")))
        self.assertEqual(self.call("POST", "/api/content?path=README.md")[0], 404)  # no other verbs

    def test_everything_else_is_refused(self):
        bad = ["", "README", "../README.md", "docs/../README.md", "/etc/passwd", "C:/Windows/win.ini", "docs\\glossary.md",
               "%2e%2e/README.md", "tools/learning_cockpit/app.py", "tools/learning_cockpit/data/progress.db",
               "topics/04_llm_engineering/17_training_loop/main.py", "topics/04_llm_engineering", "docs", ".git/config",
               "tools/hardware_report.py", "docs/nonexistent.md", "requirements.txt", "README.md\x00.png"]
        for path in bad:
            status, _ = self.call("GET", "/api/content?path=" + urllib.parse.quote(path, safe=""))
            self.assertEqual(status, 404, repr(path))
        self.assertEqual(self.call("GET", "/api/content")[0], 404)
        self.assertEqual(self.call("GET", "/api/content?path=README.md", host="evil.example")[0], 403)

    def test_allowlist_is_only_markdown_listed_in_the_catalog(self):
        allowed = content_paths(self.catalog)
        self.assertTrue(all(p.endswith(".md") and (REPO_ROOT / p).is_file() for p in allowed))
        served = json.loads(self.call("GET", "/api/catalog")[1])
        self.assertEqual(set(served["content_paths"]), allowed)
        self.assertEqual(served["evidence_kinds"], list(EVIDENCE_KINDS))
        for n in self.catalog["nodes"]:
            if n.get("content_path"):
                self.assertIn(n["content_path"], allowed)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "progress.db"
        self.ids = [n["id"] for n in load_catalog()["nodes"]]
        self.store = Store(self.db, self.ids)
        self.node = self.ids[0]

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def test_default_is_pending_and_update_works(self):
        self.assertEqual(self.store.snapshot()["status"], {})
        self.store.set_status(self.node, "studying")
        self.assertEqual(self.store.snapshot()["status"][self.node], "studying")

    def test_test_evidence_does_not_promote_mastery(self):
        self.store.add_evidence(self.node, "test", "unit tests pass")
        self.assertEqual(self.store.snapshot()["status"], {})  # still implicitly pending
        self.store.set_status(self.node, "practiced")
        self.store.add_evidence(self.node, "test", "tests pass again")
        self.assertEqual(self.store.snapshot()["status"][self.node], "practiced")

    def test_current_target_is_independent_of_mastery(self):
        self.store.set_plan(next_node_id=self.node)
        snap = self.store.snapshot()
        self.assertEqual(snap["plan"]["next_node_id"], self.node)
        self.assertEqual(snap["status"], {})
        self.store.set_plan(next_node_id=self.ids[1])
        self.assertEqual(self.store.snapshot()["plan"]["next_node_id"], self.ids[1])
        self.store.close()
        self.store = Store(self.db, self.ids)
        self.assertEqual(self.store.snapshot()["plan"]["next_node_id"], self.ids[1])

    def test_validated_requires_evidence(self):
        with self.assertRaises(ValidationError):
            self.store.set_status(self.node, "validated")
        self.store.add_evidence(self.node, "comment", "explained it aloud")
        self.store.set_status(self.node, "validated")
        self.assertEqual(self.store.snapshot()["status"][self.node], "validated")

    def test_invalid_data_rejected(self):
        bad = [
            lambda: self.store.set_status("nope", "studying"),
            lambda: self.store.set_status(self.node, "mastered"),
            lambda: self.store.add_evidence(self.node, "bogus", "x"),
            lambda: self.store.add_evidence(self.node, "comment", "   "),
            lambda: self.store.add_evidence(self.node, "comment", 5),
            lambda: self.store.add_evidence(self.node, "comment", "x" * 5000),
            lambda: self.store.add_evidence(self.node, "file", "x", "../../etc/passwd"),
            lambda: self.store.add_evidence(self.node, "file", "x", "no/such/file.py"),
            lambda: self.store.set_plan(next_node_id="nope"),
            lambda: self.store.add_session("x", "nope"),
            lambda: self.store.add_task(""),
            lambda: self.store.set_task_done(999, True),
        ]
        for fn in bad:
            with self.assertRaises(ValidationError):
                fn()

    def test_evidence_survives_status_changes_and_reopen(self):
        self.store.add_evidence(self.node, "file", "my exercise", "README.md")
        self.store.set_status(self.node, "validated")
        self.store.set_status(self.node, "practiced")
        self.store.set_plan(next_node_id=self.node, next_text="redo exercise")
        self.store.close()
        self.store = Store(self.db, self.ids)  # simulated restart
        ev = self.store.evidence(self.node)
        self.assertEqual([(e["kind"], e["text"], e["ref"]) for e in ev], [("file", "my exercise", "README.md")])
        snap = self.store.snapshot()
        self.assertEqual(snap["status"][self.node], "practiced")
        self.assertEqual(snap["plan"]["next_text"], "redo exercise")
        self.assertNotEqual(snap["last_activity"], "")

    def test_existing_database_not_overwritten(self):
        self.store.set_status(self.node, "studying")
        self.store.close()
        self.store = Store(self.db, self.ids)
        self.assertEqual(self.store.snapshot()["status"][self.node], "studying")

    def test_newer_schema_refused(self):
        self.store.conn.execute("PRAGMA user_version = 99")
        self.store.conn.commit()
        self.store.close()
        with self.assertRaises(RuntimeError):
            Store(self.db, self.ids)
        self.store = Store(Path(self.tmp.name) / "other.db", self.ids)

    def test_tasks_and_sessions(self):
        t = self.store.add_task("read README")
        self.assertEqual(self.store.set_task_done(t["id"], True)["done"], 1)
        self.store.add_session("did stuff", self.node)
        snap = self.store.snapshot()
        self.assertEqual(snap["sessions"][0]["node_id"], self.node)
        self.assertEqual(len(snap["tasks"]), 1)


class AppTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.server = create_server("127.0.0.1", 0, self.tmp.name)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.server.store.close()
        self.tmp.cleanup()

    def request(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        hdrs = dict(headers or {})
        data = None
        if body is not None:
            data = json.dumps(body)
            hdrs.setdefault("Content-Type", "application/json")
        conn.request(method, path, data, hdrs)
        res = conn.getresponse()
        raw = res.read()
        conn.close()
        return res.status, raw

    def test_binds_loopback_only(self):
        self.assertEqual(self.server.server_address[0], "127.0.0.1")
        for host in ("0.0.0.0", "192.168.1.5", ""):
            with self.assertRaises(ValueError):
                create_server(host, 0, self.tmp.name)

    def test_navigation_pages_and_api(self):
        for path in ("/", "/app.js", "/style.css"):
            status, body = self.request("GET", path)
            self.assertEqual(status, 200, path)
            self.assertTrue(body)
        status, body = self.request("GET", "/api/catalog")
        catalog = json.loads(body)
        self.assertEqual(status, 200)
        self.assertEqual(len(catalog["exercises"]), 29)
        self.assertTrue(catalog["technologies"])
        self.assertEqual(catalog["default_target"], "llm.generation")
        self.assertEqual(catalog["completed_through"]["node"], "llm.training_loop")
        self.assertEqual(len(catalog["tracks"]), 4)
        state = json.loads(self.request("GET", "/api/state")[1])
        self.assertEqual(state["status"], {})  # overlay never writes mastery
        node = catalog["nodes"][0]["id"]
        status, body = self.request("GET", f"/api/nodes/{node}")
        self.assertEqual((status, json.loads(body)["status"]), (200, "pending"))
        self.assertEqual(self.request("GET", "/api/nodes/nope")[0], 404)
        self.assertEqual(self.request("GET", "/nope")[0], 404)

    def test_no_arbitrary_file_access(self):
        for path in ("/../app.py", "/%2e%2e/app.py", "/app.py", "/data/progress.db",
                     "/static/../store.py", "/catalog/catalog.json"):
            self.assertEqual(self.request("GET", path)[0], 404, path)

    def test_status_persists_across_server_restart(self):
        node = "ml.decision_tree"
        status, _ = self.request("POST", f"/api/nodes/{node}/status", {"status": "studying"})
        self.assertEqual(status, 200)
        self.request("POST", "/api/plan", {"next_node_id": node, "next_text": "run the tree again"})
        self.server.shutdown()
        self.server.server_close()
        self.server.store.close()
        self.server = create_server("127.0.0.1", 0, self.tmp.name)
        self.port = self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        state = json.loads(self.request("GET", "/api/state")[1])
        self.assertEqual(state["status"][node], "studying")
        self.assertEqual(state["plan"]["next_text"], "run the tree again")

    def test_invalid_requests_rejected(self):
        node = "ml.decision_tree"
        self.assertEqual(self.request("POST", f"/api/nodes/{node}/status", {"status": "validated"})[0], 400)
        self.assertEqual(self.request("POST", f"/api/nodes/{node}/status", {"status": "x"})[0], 400)
        self.assertEqual(self.request("POST", "/api/nodes/nope/status", {"status": "studying"})[0], 400)
        self.assertEqual(self.request("POST", "/api/nowhere", {})[0], 404)
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request("POST", "/api/tasks", "not json", {"Content-Type": "application/json"})
        self.assertEqual(conn.getresponse().status, 400)
        conn.close()
        # wrong content type (what a cross-site HTML form would send)
        self.assertEqual(self.request("POST", "/api/tasks", {"text": "x"},
                                      {"Content-Type": "text/plain"})[0], 400)
        # foreign origin and foreign Host header
        self.assertEqual(self.request("POST", "/api/tasks", {"text": "x"},
                                      {"Origin": "http://evil.example"})[0], 400)
        self.assertEqual(self.request("GET", "/api/state", headers={"Host": "evil.example"})[0], 403)


if __name__ == "__main__":
    unittest.main()
