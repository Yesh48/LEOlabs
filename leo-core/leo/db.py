"""
leo/db.py
Handles database operations for LEO Core — supports SQLite (default)
and optional PostgreSQL (via environment variables).
"""

import os
import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional

import psycopg2
from psycopg2.extras import RealDictCursor


DB_ENGINE = os.getenv("LEO_DB_ENGINE", "sqlite")  # 'sqlite' or 'postgres'
SQLITE_PATH = os.getenv("LEO_SQLITE_PATH", "/tmp/leo.db")

POSTGRES_CONFIG = {
    "host": os.getenv("LEO_PG_HOST", "localhost"),
    "user": os.getenv("LEO_PG_USER", "leo"),
    "password": os.getenv("LEO_PG_PASSWORD", "leo123"),
    "database": os.getenv("LEO_PG_DATABASE", "leodb"),
}


def get_connection():
    """Return a database connection depending on engine."""
    if DB_ENGINE == "postgres":
        return psycopg2.connect(**POSTGRES_CONFIG, cursor_factory=RealDictCursor)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the scores table."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            rank FLOAT,
            timestamp TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def save_score(url: str, rank: float) -> None:
    """Insert a new score entry."""
    conn = get_connection()
    cur = conn.cursor()
    ts = datetime.utcnow().isoformat()
    cur.execute(
        "INSERT INTO scores (url, rank, timestamp) VALUES (?, ?, ?)"
        if DB_ENGINE == "sqlite"
        else "INSERT INTO scores (url, rank, timestamp) VALUES (%s, %s, %s)",
        (url, rank, ts),
    )
    conn.commit()
    conn.close()


def get_recent_scores(limit: int = 10) -> List[Tuple[str, float, str]]:
    """Fetch recent audit results."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT url, rank, timestamp FROM scores ORDER BY id DESC LIMIT ?"
        if DB_ENGINE == "sqlite"
        else "SELECT url, rank, timestamp FROM scores ORDER BY id DESC LIMIT %s",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


# Initialize DB automatically on import
init_db()
