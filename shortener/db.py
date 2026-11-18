"""Tiny SQLite helper."""
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS urls (
    code TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    clicks INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""


def get_conn(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn
