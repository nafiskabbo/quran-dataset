#!/usr/bin/env python3
"""
Validate data/quran.db: row counts (114 surahs, 6236 verses), required fields, verse_key format.
Exit 0 if valid, non-zero and print errors otherwise.
"""
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lib.db import get_connection, get_db_path


VERSE_KEY_RE = re.compile(r"^[1-9]\d?:[1-9]\d*$")
EXPECTED_SURAHS = 114
EXPECTED_VERSES = 6236


def main() -> int:
    db_path = get_db_path()
    if not db_path.exists():
        print(f"ERROR: Database not found: {db_path}", file=sys.stderr)
        return 1
    conn = get_connection(db_path)
    errors = []
    try:
        # Surah count
        n_surah = conn.execute("SELECT COUNT(*) FROM surahs").fetchone()[0]
        if n_surah != EXPECTED_SURAHS:
            errors.append(f"Expected {EXPECTED_SURAHS} surahs, found {n_surah}")

        # Verse count
        n_verses = conn.execute("SELECT COUNT(*) FROM verses").fetchone()[0]
        if n_verses != EXPECTED_VERSES:
            errors.append(f"Expected {EXPECTED_VERSES} verses, found {n_verses}")

        # Verse keys: format and non-null
        bad_keys = conn.execute(
            "SELECT verse_key FROM verses WHERE verse_key IS NULL OR verse_key = '' OR verse_key NOT GLOB '[0-9]*:[0-9]*'"
        ).fetchall()
        if bad_keys:
            errors.append(f"Invalid or missing verse_key: {len(bad_keys)} rows")

        # Required: text_uthmani non-empty
        empty_arabic = conn.execute("SELECT COUNT(*) FROM verses WHERE text_uthmani IS NULL OR trim(text_uthmani) = ''").fetchone()[0]
        if empty_arabic:
            errors.append(f"Verses with empty text_uthmani: {empty_arabic}")

        # Referential: every verse_key in translations should exist in verses
        orphan_tr = conn.execute(
            """SELECT COUNT(*) FROM translations t WHERE NOT EXISTS (SELECT 1 FROM verses v WHERE v.verse_key = t.verse_key)"""
        ).fetchone()[0]
        if orphan_tr:
            errors.append(f"Translations referencing missing verse_key: {orphan_tr}")

        if errors:
            for e in errors:
                print(f"ERROR: {e}", file=sys.stderr)
            return 1
        print("Validation passed: 114 surahs, 6236 verses, schema OK.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
