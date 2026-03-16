"""Database helpers for quran-dataset."""
import os
import sqlite3
from pathlib import Path


def get_data_dir() -> Path:
    """Return the repo data directory (parent of scripts/)."""
    return Path(__file__).resolve().parent.parent.parent / "data"


def get_db_path() -> Path:
    """Return path to data/quran.db."""
    return get_data_dir() / "quran.db"


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Open a connection to the canonical SQLite DB."""
    path = db_path or get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def execute_script(conn: sqlite3.Connection, sql_path: Path) -> None:
    """Execute a .sql file (multiple statements)."""
    sql = sql_path.read_text(encoding="utf-8")
    conn.executescript(sql)
