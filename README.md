# quran-dataset

An open-source Quran dataset with tools to export verses, translations, transliteration, audio, and metadata into JSON, CSV, or custom formats.

Designed for apps, APIs, and research. **Offline-first, no API key required.**

## Quick start

```bash
# Optional: use a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# Install script dependencies
pip install -r scripts/requirements.txt

# Validate the dataset
python scripts/validate.py

# Export to JSON or CSV
python scripts/export.py --format json --output exports/quran.json
python scripts/export.py --format csv --output exports/quran.csv --fields verse_key,text_uthmani,translation_en
```

See [docs/EXPORT_USAGE.md](docs/EXPORT_USAGE.md) for more examples and options.

## Features

- Complete Quran text (Arabic, Uthmani script)
- Multiple translations support (English, with roadmap for **Bengali**, **Urdu**, **French**, **Indonesian**, and more where licenses permit)
- Transliteration support in the canonical DB schema (e.g. English / Latin), ready for ingest from open transliteration sources
- Audio support in the canonical DB schema (per-verse audio and optional timestamps) with room for multiple reciters
- Surah & ayah metadata (juz, page, revelation place)
- Export formats: JSON (nested or flat), CSV, custom
- Field-level selection
- Scriptable pipeline (Python)
- Validation script and CI (GitHub Action runs `validate.py` on push/PR)
- Dataset versioning (`data/version.json`)
- Clear [data sources and attribution](docs/DATA_SOURCES.md)

## Feature checklist

- [x] Canonical SQLite database (`data/quran.db`) and JSON mirrors under `data/`
- [x] Complete Quran text (Arabic, Uthmani script)
- [x] Base translation support (e.g. English) with extensible schema for more languages
- [x] Additional translations: Bengali
- [x] Additional translations: Urdu
- [x] Additional translations: French
- [x] Additional translations: Indonesian
- [x] Transliteration support in schema (`transliterations` table)
- [x] Populate transliteration data from open, well-attributed sources (e.g. Tanzil transliteration)
- [x] Audio support in schema (`audio` table with verse-level links and optional timestamps)
- [x] Populate audio metadata and sample exports for one or more reciters (subject to licensing)
- [x] Surah & ayah metadata (juz, page, revelation place)
- [x] Export script with JSON/CSV and field selection
- [x] Validation script (`scripts/validate.py`)
- [x] Docs: schema, export usage, and data sources
- [x] Dataset versioning (`data/version.json`)

## Documentation

- [Data sources and attribution](docs/DATA_SOURCES.md) — Where data comes from and how to credit it
- [Translations and transliterations](docs/TRANSLATIONS.md) — Editions, language codes, and identifiers stored in the DB
- [Schema](docs/SCHEMA.md) — Canonical tables and fields
- [Export usage](docs/EXPORT_USAGE.md) — How to run the export script
- [Contributing](CONTRIBUTING.md) — How to run ingest/export/validate and add sources

## License

MIT License. Quran text and translations have their own licenses and attribution requirements; see [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md).

## Contributing

Contributions are welcome. Please ensure authenticity and verification of sources. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Star the repo

If you find it useful, please star the repo.
