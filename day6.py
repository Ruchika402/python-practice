#!/usr/bin/env python3
"""
Task Manager CLI — a complete command-line task management app.
Demonstrates: OOP, dataclasses, sqlite3, argparse, logging, regex, datetime
"""
import sqlite3
import logging
import argparse
import re
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional, List
from contextlib import contextmanager
from enum import Enum
from string import Template


# ===== ENUMS & DATACLASSES =====

class Priority(Enum):
    LOW    = 1
    MEDIUM = 2
    HIGH   = 3
    URGENT = 4

    def __str__(self):
        return self.name.capitalize()

@dataclass
class Task:
    title:       str
    priority:    Priority = Priority.MEDIUM
    due_date:    Optional[date] = None
    tags:        List[str] = field(default_factory=list)
    completed:   bool = False
    id:          Optional[int] = None
    created_at:  datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 200:
            raise ValueError("Title too long (max 200 chars)")

    def is_overdue(self) -> bool:
        if self.due_date and not self.completed:
            return self.due_date < date.today()
        return False

    def days_until_due(self) -> Optional[int]:
        if not self.due_date:
            return None
        return (self.due_date - date.today()).days

    def __str__(self) -> str:
        status = "DONE" if self.completed else ("OVERDUE" if self.is_overdue() else "OPEN")
        due = f" | Due: {self.due_date}" if self.due_date else ""
        tags = f" | Tags: {','.join(self.tags)}" if self.tags else ""
        return (f"[{self.id}] [{status}] [{self.priority}] {self.title}"
                f"{due}{tags}")

# ===== DATABASE LAYER =====

@contextmanager
def get_connection(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

class TaskRepository:
    def __init__(self, db_path: str = "tasks.db"):
        self.db = db_path
        self.log = logging.getLogger(self.__class__.__name__)
        self._init_schema()

    def _init_schema(self):
        with get_connection(self.db) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    title       TEXT    NOT NULL,
                    priority    INTEGER NOT NULL DEFAULT 2,
                    due_date    TEXT,
                    tags        TEXT    DEFAULT '',
                    completed   INTEGER DEFAULT 0,
                    created_at  TEXT    NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_priority  ON tasks(priority);
                CREATE INDEX IF NOT EXISTS idx_completed ON tasks(completed);
                CREATE INDEX IF NOT EXISTS idx_due_date  ON tasks(due_date);
            """)
        self.log.info("Database initialized")

    def add(self, task: Task) -> int:
        with get_connection(self.db) as conn:
            cur = conn.execute(
                """INSERT INTO tasks (title,priority,due_date,tags,completed,created_at)
                   VALUES (?,?,?,?,?,?)""",
                (task.title, task.priority.value,
                 str(task.due_date) if task.due_date else None,
                 ",".join(task.tags), int(task.completed),
                 task.created_at.isoformat())
            )
            self.log.info(f"Added task id={cur.lastrowid}: '{task.title}'")
            return cur.lastrowid

    def _row_to_task(self, row) -> Task:
        return Task(
            id=row["id"],
            title=row["title"],
            priority=Priority(row["priority"]),
            due_date=date.fromisoformat(row["due_date"]) if row["due_date"] else None,
            tags=[t for t in row["tags"].split(",") if t],
            completed=bool(row["completed"]),
            created_at=datetime.fromisoformat(row["created_at"])
        )

    def get_all(self, include_done: bool = False) -> List[Task]:
        query = "SELECT * FROM tasks"
        if not include_done:
            query += " WHERE completed = 0"
        query += " ORDER BY priority DESC, due_date ASC NULLS LAST"
        with get_connection(self.db) as conn:
            return [self._row_to_task(r) for r in conn.execute(query).fetchall()]

    def search(self, keyword: str) -> List[Task]:
        pattern = f"%{keyword}%"
        with get_connection(self.db) as conn:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE title LIKE ? OR tags LIKE ?",
                (pattern, pattern)
            ).fetchall()
            return [self._row_to_task(r) for r in rows]

    def complete(self, task_id: int) -> bool:
        with get_connection(self.db) as conn:
            cur = conn.execute(
                "UPDATE tasks SET completed=1 WHERE id=?", (task_id,)
            )
            done = cur.rowcount > 0
        if done: self.log.info(f"Completed task id={task_id}")
        return done

    def delete(self, task_id: int) -> bool:
        with get_connection(self.db) as conn:
            cur = conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            return cur.rowcount > 0

    def stats(self) -> dict:
        with get_connection(self.db) as conn:
            row = conn.execute("""
                SELECT
                    COUNT(*) total,
                    SUM(completed) done,
                    SUM(CASE WHEN completed=0 AND due_date < date('now') THEN 1 ELSE 0 END) overdue,
                    SUM(CASE WHEN priority=4 AND completed=0 THEN 1 ELSE 0 END) urgent
                FROM tasks
            """).fetchone()
            return dict(row)

# ===== SERVICE LAYER =====

DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def add_task(self, title: str, priority: str = "medium",
                 due: Optional[str] = None, tags: str = "") -> Task:
        try:
            p = Priority[priority.upper()]
        except KeyError:
            raise ValueError(f"Invalid priority. Choose: {[p.name.lower() for p in Priority]}")

        due_date = None
        if due:
            if not DATE_RE.match(due):
                raise ValueError("Due date must be YYYY-MM-DD format")
            due_date = date.fromisoformat(due)

        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        task = Task(title=title, priority=p, due_date=due_date, tags=tag_list)
        task.id = self.repo.add(task)
        return task

    def get_summary(self) -> str:
        s = self.repo.stats()
        pending = s['total'] - s['done']
        return (f"Total: {s['total']} | Pending: {pending} | "
                f"Done: {s['done']} | Overdue: {s['overdue']} | Urgent: {s['urgent']}")

# ===== CLI =====

def build_cli(service: TaskService) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tasks",
        description="Task Manager — keep track of your work"
    )
    sub = parser.add_subparsers(dest="command")

    # add subcommand
    add_p = sub.add_parser("add", help="Add a new task")
    add_p.add_argument("title")
    add_p.add_argument("--priority", "-p", default="medium",
                       choices=["low","medium","high","urgent"])
    add_p.add_argument("--due", "-d", help="Due date YYYY-MM-DD")
    add_p.add_argument("--tags", "-t", default="", help="Comma-separated tags")

    sub.add_parser("list", help="List all open tasks")
    sub.add_parser("all",  help="List all tasks including completed")

    done_p = sub.add_parser("done", help="Mark task as complete")
    done_p.add_argument("id", type=int)

    del_p = sub.add_parser("delete", help="Delete a task")
    del_p.add_argument("id", type=int)

    search_p = sub.add_parser("search", help="Search tasks")
    search_p.add_argument("keyword")

    sub.add_parser("stats", help="Show statistics")
    return parser

def run_cli(args, service: TaskService):
    if args.command == "add":
        task = service.add_task(args.title, args.priority, args.due, args.tags)
        print(f"Added: {task}")
    elif args.command in ("list", "all"):
        tasks = service.repo.get_all(include_done=(args.command=="all"))
        if not tasks:
            print("No tasks found.")
        for t in tasks:
            print(t)
    elif args.command == "done":
        print("Done!" if service.repo.complete(args.id) else "Task not found")
    elif args.command == "delete":
        print("Deleted!" if service.repo.delete(args.id) else "Task not found")
    elif args.command == "search":
        results = service.repo.search(args.keyword)
        print(f"Found {len(results)} task(s):")
        for t in results: print(t)
    elif args.command == "stats":
        print(service.get_summary())
    else:
        print("Use --help to see available commands")

# Demo run (normally: parse sys.argv)
if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    repo    = TaskRepository(":memory:")
    service = TaskService(repo)
    parser  = build_cli(service)

    # Simulate command: tasks add "Build Django project" -p high -d 2024-12-31 -t python,web
    class Args:
        command="add"; title="Build Django project"
        priority="high"; due="2024-12-31"; tags="python,web"
    run_cli(Args(), service)

    class Args2:
        command="add"; title="Study OOP patterns"
        priority="urgent"; due=None; tags="python"
    run_cli(Args2(), service)

    class Args3: command="list"
    run_cli(Args3(), service)

    class Args4: command="stats"
    run_cli(Args4(), service)