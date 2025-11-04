"""Database utilities for Leo Core."""
from __future__ import annotations

import os
import sqlite3
from contextlib import closing
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    import psycopg2
except Exception:  # pragma: no cover - optional dependency
    psycopg2 = None  # type: ignore


SQLITE_SCORES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    rank REAL NOT NULL,
    timestamp TEXT NOT NULL
)
"""

POSTGRES_SCORES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS scores (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    rank DOUBLE PRECISION NOT NULL,
    timestamp TEXT NOT NULL
)
"""


class DatabaseError(RuntimeError):
    """Raised when the database configuration is invalid."""


class Database:
    """Minimal database wrapper supporting SQLite and Postgres."""

    def __init__(self) -> None:
        postgres_enabled = os.getenv("POSTGRES_ENABLED", "").lower() in {"1", "true", "yes"}
        self.engine = "postgres" if postgres_enabled else os.getenv("LEO_DB_ENGINE", "sqlite").lower()
        if self.engine not in {"sqlite", "postgres"}:
            raise DatabaseError(f"Unsupported database engine: {self.engine}")
        self._sqlite_path = os.getenv("LEO_DB_PATH", "/tmp/leo.db")
        self._postgres_dsn = os.getenv("LEO_DB_DSN")
        self._postgres_settings = {
            "dbname": os.getenv("LEO_DB_NAME", "leodb"),
            "user": os.getenv("LEO_DB_USER", "leo"),
            "password": os.getenv("LEO_DB_PASSWORD", ""),
            "host": os.getenv("LEO_DB_HOST", "localhost"),
            "port": int(os.getenv("LEO_DB_PORT", "5432")),
        }
        self._initialised = False

    # connection helpers -------------------------------------------------
    def connect(self):  # type: ignore[override]
        if self.engine == "sqlite":
            conn = sqlite3.connect(self._sqlite_path)
            conn.execute("PRAGMA journal_mode=WAL;")
            return conn
        if psycopg2 is None:
            raise DatabaseError("psycopg2-binary is required for Postgres support")
        if self._postgres_dsn:
            return psycopg2.connect(self._postgres_dsn)
        return psycopg2.connect(**self._postgres_settings)

    # schema --------------------------------------------------------------
    def init(self) -> None:
        if self._initialised:
            return
        with closing(self.connect()) as conn:
            cursor = conn.cursor()
            if self.engine == "postgres":
                cursor.execute(POSTGRES_SCORES_TABLE_SQL)
            else:
                cursor.execute(SQLITE_SCORES_TABLE_SQL)
            conn.commit()
        self._initialised = True

    # operations ----------------------------------------------------------
    def record_score(self, url: str, rank: float, timestamp: Optional[str] = None) -> None:
        self.init()
        ts = timestamp or datetime.utcnow().isoformat()
        with closing(self.connect()) as conn:
            cursor = conn.cursor()
            if self.engine == "postgres":
                cursor.execute(
                    "INSERT INTO scores (url, rank, timestamp) VALUES (%s, %s, %s)",
                    (url, rank, ts),
                )
            else:
                cursor.execute(
                    "INSERT INTO scores (url, rank, timestamp) VALUES (?, ?, ?)",
                    (url, rank, ts),
                )
            conn.commit()

    def recent_scores(self, limit: int = 10) -> List[Dict[str, Any]]:
        self.init()
        if self.engine == "postgres":
            query = "SELECT id, url, rank, timestamp FROM scores ORDER BY timestamp DESC LIMIT %s"
            params = (limit,)
        else:
            query = "SELECT id, url, rank, timestamp FROM scores ORDER BY timestamp DESC LIMIT ?"
            params = (limit,)
        with closing(self.connect()) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
        results: List[Dict[str, Any]] = []
        for row in rows:
            if self.engine == "postgres":
                record_id, url, rank, timestamp = row
            else:
                record_id, url, rank, timestamp = row
            results.append(
                {
                    "id": int(record_id),
                    "url": url,
                    "rank": float(rank),
                    "timestamp": str(timestamp),
                }
            )
        return results

    def summary(self) -> Dict[str, Any]:
        self.init()
        with closing(self.connect()) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), AVG(rank) FROM scores")
            count, average = cursor.fetchone()
        return {
            "engine": self.engine,
            "count": int(count or 0),
            "average_rank": float(average or 0.0),
        }


_DB_INSTANCE: Optional[Database] = None


def get_database() -> Database:
    """Return a singleton database instance."""
    global _DB_INSTANCE
    if _DB_INSTANCE is None:
        _DB_INSTANCE = Database()
        _DB_INSTANCE.init()
    return _DB_INSTANCE


__all__ = ["Database", "DatabaseError", "get_database"]
