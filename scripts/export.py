#!/usr/bin/env python3
"""
Export the canonical dataset to JSON, CSV, or custom format.
Usage: python scripts/export.py --format json --output path [--fields ...] [--surah 1-3] [--lang en] [--include-attribution]
"""
import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lib.db import get_db_path
from lib.export_formats import export_json, export_csv, export_custom, get_attribution_text


def parse_surah_range(s: str) -> list[int] | None:
    """Parse --surah 1-3 or 1,2,3 into list of surah numbers."""
    if not s or s.strip() == "":
        return None
    out = []
    for part in s.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a.strip()), int(b.strip()) + 1))
        else:
            out.append(int(part))
    return sorted(set(out)) if out else None


def main() -> int:
    ap = argparse.ArgumentParser(description="Export quran-dataset to JSON, CSV, or custom format.")
    ap.add_argument("--format", "-f", choices=["json", "csv", "custom"], default="json", help="Output format")
    ap.add_argument("--output", "-o", type=Path, required=True, help="Output file path")
    ap.add_argument("--fields", type=str, default=None, help="Comma-separated field list (e.g. verse_key,text_uthmani,translation_en)")
    ap.add_argument("--surah", type=str, default=None, help="Limit to surahs: 1-3 or 1,2,3")
    ap.add_argument("--lang", type=str, default="en", help="Translation language code for translation_* field (default en)")
    ap.add_argument("--shape", type=str, choices=["nested", "flat"], default="nested", help="JSON shape (default nested)")
    ap.add_argument("--include-attribution", action="store_true", help="Append data sources attribution to output")
    ap.add_argument("--delimiter", type=str, default="|", help="Custom format delimiter (default |)")
    args = ap.parse_args()

    db_path = get_db_path()
    if not db_path.exists():
        print(f"Database not found: {db_path}. Run scripts/ingest.py first.", file=sys.stderr)
        return 1

    fields = [x.strip() for x in args.fields.split(",")] if args.fields else None
    surah_range = parse_surah_range(args.surah) if args.surah else None
    lang = args.lang if (fields and "translation_en" in fields) or not fields else args.lang

    try:
        if args.format == "json":
            export_json(
                args.output,
                shape=args.shape,
                surah_range=surah_range,
                lang=lang,
                fields=fields,
                include_attribution=args.include_attribution,
                db_path=db_path,
            )
        elif args.format == "csv":
            export_csv(
                args.output,
                surah_range=surah_range,
                lang=lang,
                fields=fields,
                include_attribution=args.include_attribution,
                db_path=db_path,
            )
        else:
            export_custom(
                args.output,
                delimiter=args.delimiter,
                columns=fields,
                surah_range=surah_range,
                lang=lang,
                include_attribution=args.include_attribution,
                db_path=db_path,
            )
        print(f"Wrote {args.output}")
        return 0
    except Exception as e:
        print(f"Export failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
