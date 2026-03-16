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
- Multiple translations support
- Transliteration (e.g. English / Latin)
- Audio support and audio timestamp support
- Surah & ayah metadata (juz, page, revelation place)
- Export formats: JSON (nested or flat), CSV, custom
- Field-level selection
- Scriptable pipeline (Python)
- Validation script and CI (GitHub Action runs `validate.py` on push/PR)
- Dataset versioning (`data/version.json`)
- Clear [data sources and attribution](docs/DATA_SOURCES.md)

## Documentation

- [Data sources and attribution](docs/DATA_SOURCES.md) — Where data comes from and how to credit it
- [Schema](docs/SCHEMA.md) — Canonical tables and fields
- [Export usage](docs/EXPORT_USAGE.md) — How to run the export script
- [Contributing](CONTRIBUTING.md) — How to run ingest/export/validate and add sources

## License

MIT License. Quran text and translations have their own licenses and attribution requirements; see [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md).

## Contributing

Contributions are welcome. Please ensure authenticity and verification of sources. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Star the repo

If you find it useful, please star the repo.
