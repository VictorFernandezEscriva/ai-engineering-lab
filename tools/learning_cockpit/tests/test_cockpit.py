import copy
import http.client
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_server  # noqa: E402
from catalog import CATALOG_PATH, REPO_ROOT, CatalogError, load_catalog, validate  # noqa: E402
from store import Store, ValidationError  # noqa: E402


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
        for area_id in ("later", "cross"):  # visual groupings, not one lane per phase
            self.assertNotIn("path", next(a for a in self.catalog["areas"] if a["id"] == area_id))
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
        self.assertIn("Experiment 30 — Autoregressive Generation and Sampling", roadmap)
        self.assertIn("**Status:** NEXT", roadmap)

    def test_completed_through_overlay_is_consistent(self):
        done = self.catalog["completed_through"]
        self.assertEqual(done["node"], "llm.training_loop")
        covered = {n["id"] for n in self.catalog["nodes"] if n["exercises"]}  # same rule as the UI
        self.assertIn(done["node"], covered)
        self.assertNotIn(self.catalog["default_target"], covered)  # target is not yet covered
        for nid in covered:  # covered set is closed under prerequisites
            self.assertTrue(set(self.nodes[nid]["prerequisites"]) <= covered, nid)
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("## Experiment 29 — Language-Model Training Loop\n\n**Status:** COMPLETE", roadmap)
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
