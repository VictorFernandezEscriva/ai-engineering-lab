"""Learning Cockpit: local web UI over the curriculum catalog and personal progress.

Standard library only. Listens on loopback; serves three fixed static files and a
small JSON API. It never reads arbitrary paths and never runs commands.
"""
import argparse
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from catalog import REPO_ROOT, load_catalog
from store import Store, ValidationError

HERE = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = HERE / "data"
STATIC = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
}
LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}
MAX_BODY = 64 * 1024
NODE_RE = re.compile(r"^/api/nodes/([A-Za-z0-9_.-]+)(/status|/evidence)?$")
TASK_RE = re.compile(r"^/api/tasks/(\d+)$")


def _host_only(header):
    header = (header or "").strip()
    if header.startswith("["):
        return header[1:header.find("]")] if "]" in header else ""
    return header.rsplit(":", 1)[0] if header.count(":") == 1 else header


def make_handler(catalog, store):
    nodes = {n["id"]: n for n in catalog["nodes"]}

    class Handler(BaseHTTPRequestHandler):
        server_version = "LearningCockpit"

        def log_message(self, fmt, *args):  # keep the terminal quiet
            pass

        def _send(self, status, body, content_type="application/json; charset=utf-8"):
            if not isinstance(body, bytes):
                body = json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'")
            self.end_headers()
            self.wfile.write(body)

        def _error(self, status, message):
            self._send(status, {"error": message})

        def _host_ok(self):
            if _host_only(self.headers.get("Host")) not in LOOPBACK_HOSTS:
                self._error(403, "forbidden host")
                return False
            return True

        def do_GET(self):
            if not self._host_ok():
                return
            path = self.path.split("?", 1)[0]
            if path in STATIC:
                name, ctype = STATIC[path]
                self._send(200, (HERE / "static" / name).read_bytes(), ctype)
            elif path == "/api/catalog":
                self._send(200, catalog)
            elif path == "/api/state":
                self._send(200, store.snapshot())
            else:
                match = NODE_RE.match(path)
                if match and not match.group(2) and match.group(1) in nodes:
                    self._send(200, {"node": nodes[match.group(1)],
                                     "status": store.snapshot()["status"].get(match.group(1), "pending"),
                                     "evidence": store.evidence(match.group(1))})
                else:
                    self._error(404, "not found")

        def _read_json(self):
            if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
                raise ValidationError("Content-Type must be application/json")
            origin = self.headers.get("Origin")
            if origin and _host_only(origin.split("://", 1)[-1]) not in LOOPBACK_HOSTS:
                raise ValidationError("cross-origin request refused")
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                length = -1
            if not 0 < length <= MAX_BODY:
                raise ValidationError("invalid body size")
            try:
                data = json.loads(self.rfile.read(length))
            except ValueError:
                raise ValidationError("invalid JSON")
            if not isinstance(data, dict):
                raise ValidationError("JSON body must be an object")
            return data

        def do_POST(self):
            if not self._host_ok():
                return
            path = self.path.split("?", 1)[0]
            try:
                data = self._read_json()
                result = self._route_post(path, data)
            except ValidationError as exc:
                return self._error(400, str(exc))
            if result is None:
                return self._error(404, "not found")
            self._send(200, result)

        def _route_post(self, path, data):
            match = NODE_RE.match(path)
            if match and match.group(2) == "/status":
                return store.set_status(match.group(1), data.get("status"))
            if match and match.group(2) == "/evidence":
                return store.add_evidence(match.group(1), data.get("kind"), data.get("text"), data.get("ref", ""))
            if path == "/api/plan":
                return store.set_plan(data.get("goal"), data.get("next_node_id"), data.get("next_text"))
            if path == "/api/sessions":
                return store.add_session(data.get("note"), data.get("node_id", ""))
            if path == "/api/tasks":
                return store.add_task(data.get("text"))
            match = TASK_RE.match(path)
            if match:
                return store.set_task_done(int(match.group(1)), data.get("done"))
            return None

    return Handler


def create_server(host="127.0.0.1", port=8765, data_dir=DEFAULT_DATA_DIR, repo_root=REPO_ROOT):
    if host not in LOOPBACK_HOSTS:
        raise ValueError("Learning Cockpit only listens on loopback (127.0.0.1, localhost or ::1)")
    catalog = load_catalog(root=repo_root)
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    store = Store(data_dir / "progress.db", [n["id"] for n in catalog["nodes"]], repo_root)
    server = HTTPServer((host, port), make_handler(catalog, store))
    server.store = store
    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR))
    args = parser.parse_args()
    server = create_server(args.host, args.port, args.data_dir)
    print(f"Learning Cockpit: http://{args.host}:{server.server_address[1]}/  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        server.store.close()


if __name__ == "__main__":
    main()
