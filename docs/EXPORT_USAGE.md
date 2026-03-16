# Export usage

The export script reads the canonical dataset (`data/quran.db`) and writes JSON, CSV, or custom formats with optional field selection.

## Prerequisites

```bash
pip install -r scripts/requirements.txt
```

## Basic usage

```bash
# Full Quran as nested JSON (surahs → verses)
python scripts/export.py --format json --output exports/quran.json

# Full Quran as flat JSON (one object per verse)
python scripts/export.py --format json --output exports/quran_flat.json --shape flat

# CSV with selected fields
python scripts/export.py --format csv --output exports/quran.csv --fields verse_key,text_uthmani,translation_en

# Include attribution block in the output file
python scripts/export.py --format json --output exports/quran.json --include-attribution
```

## Options

| Option | Description |
|--------|-------------|
| `--format` | `json`, `csv`, or `custom` |
| `--output` | Output file path |
| `--fields` | Comma-separated list of fields (e.g. `verse_key,text_uthmani,translation_en`) |
| `--surah` | Limit to surahs: `1-3` or `1,2,3` |
| `--lang` | Filter translations by language code (e.g. `en`) |
| `--shape` | For JSON: `nested` (default) or `flat` |
| `--include-attribution` | Append data sources attribution to the output |

## Examples

**Minimal JSON (verse_key, Arabic text, one translation):**
```bash
python scripts/export.py --format json --output sample_minimal.json --fields verse_key,text_uthmani,translation_en --surah 1
```

**Full CSV for research:**
```bash
python scripts/export.py --format csv --output quran_full.csv
```

**Custom format (column list + delimiter):**  
See the script help: `python scripts/export.py --help`. Custom format uses a simple column list and configurable delimiter defined in the script or config.

## Output shapes

- **nested (JSON):** `{ "surahs": [ { "id": 1, "name_ar": "...", "verses": [ ... ] } ] }`
- **flat (JSON):** Array of objects, one per verse, with surah_id, ayah_number, verse_key, and selected fields.
- **CSV:** One row per verse; column headers = selected fields.
