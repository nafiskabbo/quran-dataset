"""Export writers: JSON (nested/flat), CSV, custom."""
import csv
import json
from pathlib import Path
from typing import Any

from .db import get_connection, get_db_path


ATTRIBUTION_BLOCK = """
---
Data sources and attribution: see docs/DATA_SOURCES.md
Arabic text: Tanzil Project (https://tanzil.net/), CC BY 3.0. Do not modify.
Translations and other data: see docs/DATA_SOURCES.md for each source.
---
"""


def _get_verses(
    conn,
    surah_range: list[int] | None = None,
    lang: str | None = None,
    fields: list[str] | None = None,
) -> list[dict]:
    """Fetch verses with optional translation; return list of dicts."""
    where_sql = ""
    if surah_range is not None:
        ph = ",".join("?" * len(surah_range))
        where_sql = f"WHERE v.surah_id IN ({ph})"

    # Base verse fields
    verse_cols = [
        "v.surah_id",
        "v.ayah_number",
        "v.verse_key",
        "v.text_uthmani",
        "v.text_simple",
        "v.juz",
        "v.page",
        "v.rub_el_hizb",
        "v.sajdah",
    ]
    select_verse = ", ".join(verse_cols)

    # Optional translation for a single lang
    if lang:
        sql = f"""
        SELECT {select_verse}, t.text AS translation_text, t.translator
        FROM verses v
        LEFT JOIN translations t ON t.verse_key = v.verse_key AND t.lang_code = ?
        {" " + where_sql if where_sql else ""}
        ORDER BY v.surah_id, v.ayah_number
        """
        params: list = [lang]
        if surah_range is not None:
            params = [lang] + list(surah_range)
        rows = conn.execute(sql, params).fetchall()
    else:
        sql = f"""
        SELECT {select_verse}
        FROM verses v
        {" " + where_sql if where_sql else ""}
        ORDER BY v.surah_id, v.ayah_number
        """
        params = list(surah_range) if surah_range else []
        rows = conn.execute(sql, params).fetchall()

    out = []
    for row in rows:
        d = dict(row)
        if "translation_text" in d:
            d["translation_en"] = d.pop("translation_text", None)
        out.append(d)
    return out


def _apply_field_filter(rows: list[dict], fields: list[str] | None) -> list[dict]:
    """Keep only requested keys; translation_text already renamed to translation_en in _get_verses."""
    if not fields:
        return rows
    allowed = set(fields)
    result = []
    for r in rows:
        filtered = {k: v for k, v in r.items() if k in allowed}
        result.append(filtered)
    return result


def export_json(
    output_path: Path,
    shape: str = "nested",
    surah_range: list[int] | None = None,
    lang: str | None = None,
    fields: list[str] | None = None,
    include_attribution: bool = False,
    db_path: Path | None = None,
) -> None:
    """Write JSON: nested (surahs -> verses) or flat (array of verse objects)."""
    conn = get_connection(db_path)
    try:
        rows = _get_verses(conn, surah_range=surah_range, lang=lang, fields=fields)
        rows = _apply_field_filter(rows, fields)

        if shape == "flat":
            data: Any = rows
        else:
            # Nested: group by surah
            surahs = {}
            for r in rows:
                sid = r.get("surah_id")
                if sid not in surahs:
                    surahs[sid] = {"id": sid, "verses": []}
                surahs[sid]["verses"].append(r)
            data = {"surahs": [surahs[k] for k in sorted(surahs)]}

        text = json.dumps(data, ensure_ascii=False, indent=2)
        if include_attribution:
            text = text.rstrip() + "\n" + ATTRIBUTION_BLOCK
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
    finally:
        conn.close()


def export_csv(
    output_path: Path,
    surah_range: list[int] | None = None,
    lang: str | None = None,
    fields: list[str] | None = None,
    include_attribution: bool = False,
    db_path: Path | None = None,
) -> None:
    """Write CSV: one row per verse."""
    conn = get_connection(db_path)
    try:
        rows = _get_verses(conn, surah_range=surah_range, lang=lang, fields=fields)
        rows = _apply_field_filter(rows, fields)
        if not rows:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text("", encoding="utf-8")
            return
        headers = list(rows[0].keys())
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=headers)
            w.writeheader()
            w.writerows(rows)
        if include_attribution:
            with open(output_path, "a", encoding="utf-8") as f:
                f.write(ATTRIBUTION_BLOCK)
    finally:
        conn.close()


def export_custom(
    output_path: Path,
    delimiter: str = "|",
    columns: list[str] | None = None,
    surah_range: list[int] | None = None,
    lang: str | None = None,
    include_attribution: bool = False,
    db_path: Path | None = None,
) -> None:
    """Write custom: one line per verse, columns separated by delimiter."""
    conn = get_connection(db_path)
    try:
        rows = _get_verses(conn, surah_range=surah_range, lang=lang, fields=columns)
        rows = _apply_field_filter(rows, columns)
        cols = columns or (list(rows[0].keys()) if rows else [])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(delimiter.join(cols) + "\n")
            for r in rows:
                line = delimiter.join(str(r.get(c, "")) for c in cols)
                f.write(line + "\n")
            if include_attribution:
                f.write(ATTRIBUTION_BLOCK)
    finally:
        conn.close()


def get_attribution_text() -> str:
    """Return the attribution block for embedding in exports."""
    return ATTRIBUTION_BLOCK.strip()
