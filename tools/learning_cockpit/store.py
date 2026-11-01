"""Mutable personal progress in a local SQLite file (never versioned)."""
import sqlite3
from datetime import datetime, timezone

from catalog import resolve_repo_path, REPO_ROOT

SCHEMA_VERSION = 1
STATUSES = ("pending", "studying", "practiced", "validated")
EVIDENCE_KINDS = ("exercise", "test", "evaluation", "comment", "file")
MAX_TEXT = 2000

SCHEMA = """
CREATE TABLE IF NOT EXISTS mastery (
    node_id TEXT PRIMARY KEY, status TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT, node_id TEXT NOT NULL, kind TEXT NOT NULL,
    text TEXT NOT NULL, ref TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS plan (
    id INTEGER PRIMARY KEY CHECK (id = 1), goal TEXT NOT NULL DEFAULT '',
    next_node_id TEXT NOT NULL DEFAULT '', next_text TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT, node_id TEXT NOT NULL DEFAULT '',
    note TEXT NOT NULL, created_at TEXT NOT NULL);
"""


class ValidationError(ValueError):
    pass


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _text(value, field, required=True):
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a string")
    value = value.strip()
    if required and not value:
        raise ValidationError(f"{field} is required")
    if len(value) > MAX_TEXT:
        raise ValidationError(f"{field} is longer than {MAX_TEXT} characters")
    return value


class Store:
    def __init__(self, db_path, node_ids, repo_root=REPO_ROOT):
        self.node_ids = set(node_ids)
        self.repo_root = repo_root
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        version = self.conn.execute("PRAGMA user_version").fetchone()[0]
        if version > SCHEMA_VERSION:
            self.conn.close()
            raise RuntimeError(f"{db_path} has newer schema v{version}; refusing to touch it")
        self.conn.executescript(SCHEMA)  # IF NOT EXISTS: an existing database is kept as is
        self.conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
        self.conn.commit()

    def close(self):
        self.conn.close()

    def _check_node(self, node_id):
        if node_id not in self.node_ids:
            raise ValidationError(f"unknown node: {node_id}")

    def _rows(self, sql, *args):
        return [dict(r) for r in self.conn.execute(sql, args)]

    def evidence(self, node_id):
        return self._rows("SELECT * FROM evidence WHERE node_id = ? ORDER BY id", node_id)

    def set_status(self, node_id, status):
        self._check_node(node_id)
        if status not in STATUSES:
            raise ValidationError(f"status must be one of {', '.join(STATUSES)}")
        if status == "validated" and not self.evidence(node_id):
            raise ValidationError("validated requires at least one piece of evidence")
        now = _now()
        self.conn.execute(
            "INSERT INTO mastery (node_id, status, updated_at) VALUES (?, ?, ?) "
            "ON CONFLICT(node_id) DO UPDATE SET status = excluded.status, updated_at = excluded.updated_at",
            (node_id, status, now))
        self.conn.commit()
        return {"node_id": node_id, "status": status, "updated_at": now}

    def add_evidence(self, node_id, kind, text, ref=""):
        self._check_node(node_id)
        if kind not in EVIDENCE_KINDS:
            raise ValidationError(f"kind must be one of {', '.join(EVIDENCE_KINDS)}")
        text = _text(text, "text")
        ref = _text(ref, "ref", required=False) if ref else ""
        if ref and resolve_repo_path(ref, self.repo_root) is None:
            raise ValidationError("ref must be an existing path inside the repository")
        cur = self.conn.execute(
            "INSERT INTO evidence (node_id, kind, text, ref, created_at) VALUES (?, ?, ?, ?, ?)",
            (node_id, kind, text, ref, _now()))
        self.conn.commit()
        return self._rows("SELECT * FROM evidence WHERE id = ?", cur.lastrowid)[0]

    def set_plan(self, goal=None, next_node_id=None, next_text=None):
        current = self.plan()
        goal = current["goal"] if goal is None else _text(goal, "goal", required=False)
        next_text = current["next_text"] if next_text is None else _text(next_text, "next_text", required=False)
        if next_node_id is None:
            next_node_id = current["next_node_id"]
        elif next_node_id:
            self._check_node(next_node_id)
        self.conn.execute(
            "INSERT INTO plan (id, goal, next_node_id, next_text, updated_at) VALUES (1, ?, ?, ?, ?) "
            "ON CONFLICT(id) DO UPDATE SET goal = excluded.goal, next_node_id = excluded.next_node_id, "
            "next_text = excluded.next_text, updated_at = excluded.updated_at",
            (goal, next_node_id, next_text, _now()))
        self.conn.commit()
        return self.plan()

    def plan(self):
        rows = self._rows("SELECT * FROM plan WHERE id = 1")
        return rows[0] if rows else {"goal": "", "next_node_id": "", "next_text": "", "updated_at": ""}

    def add_task(self, text):
        text = _text(text, "text")
        cur = self.conn.execute("INSERT INTO tasks (text, created_at) VALUES (?, ?)", (text, _now()))
        self.conn.commit()
        return self._rows("SELECT * FROM tasks WHERE id = ?", cur.lastrowid)[0]

    def set_task_done(self, task_id, done):
        if not isinstance(task_id, int) or isinstance(done, bool) is False:
            raise ValidationError("task_id must be an integer and done a boolean")
        cur = self.conn.execute("UPDATE tasks SET done = ? WHERE id = ?", (int(done), task_id))
        self.conn.commit()
        if cur.rowcount == 0:
            raise ValidationError(f"unknown task: {task_id}")
        return self._rows("SELECT * FROM tasks WHERE id = ?", task_id)[0]

    def add_session(self, note, node_id=""):
        if node_id:
            self._check_node(node_id)
        note = _text(note, "note")
        cur = self.conn.execute(
            "INSERT INTO sessions (node_id, note, created_at) VALUES (?, ?, ?)", (node_id or "", note, _now()))
        self.conn.commit()
        return self._rows("SELECT * FROM sessions WHERE id = ?", cur.lastrowid)[0]

    def snapshot(self):
        """All mutable state; nodes without a row are implicitly 'pending'."""
        sessions = self._rows("SELECT * FROM sessions ORDER BY id DESC LIMIT 20")
        stamps = [r["updated_at"] for r in self._rows("SELECT updated_at FROM mastery")]
        stamps += [r["created_at"] for r in self._rows("SELECT created_at FROM evidence")]
        stamps += [s["created_at"] for s in sessions]
        return {
            "status": {r["node_id"]: r["status"] for r in self._rows("SELECT node_id, status FROM mastery")},
            "plan": self.plan(),
            "tasks": self._rows("SELECT * FROM tasks ORDER BY done, id"),
            "sessions": sessions,
            "last_activity": max(stamps) if stamps else "",
        }
