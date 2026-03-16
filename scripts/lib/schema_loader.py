"""Load and apply the canonical schema."""
from pathlib import Path

from .db import get_connection, get_db_path


def get_schema_path() -> Path:
    """Return path to schema/schema.sql."""
    return Path(__file__).resolve().parent.parent.parent / "schema" / "schema.sql"


def init_db(conn=None) -> None:
    """Create or ensure the database and apply schema/schema.sql."""
    close = False
    if conn is None:
        conn = get_connection()
        close = True
    try:
        schema_path = get_schema_path()
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema not found: {schema_path}")
        sql = schema_path.read_text(encoding="utf-8")
        conn.executescript(sql)
        conn.commit()
    finally:
        if close:
            conn.close()
