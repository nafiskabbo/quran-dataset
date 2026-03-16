# Contributing to quran-dataset

Contributions are welcome. Please ensure authenticity and verification of sources.

## Development setup

1. Clone the repo and (optional) create a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

2. Install script dependencies:

   ```bash
   pip install -r scripts/requirements.txt
   ```

## Running scripts

- **Validate** the canonical dataset (run after any change to `data/`):

  ```bash
  python scripts/validate.py
  ```

- **Export** to JSON, CSV, or custom format:

  ```bash
  python scripts/export.py --format json --output exports/quran.json
  python scripts/export.py --format csv --output exports/quran.csv --fields verse_key,text_uthmani,translation_en
  ```

  See [docs/EXPORT_USAGE.md](docs/EXPORT_USAGE.md) for more examples.

- **Ingest** (rebuild `data/` from sources; use with care):

  ```bash
  python scripts/ingest.py
  ```

  This downloads from sources listed in `sources/config/sources.yaml`, validates, and writes to `data/quran.db` (and optionally `data/surahs.json`, `data/verses/`). Ensure you have network access. After running, commit updated `data/` if appropriate.

## Adding a new translation or source

1. Choose only sources with a **clear open license** (MIT, CC, public domain). Verify the license allows redistribution and attribution.
2. Add the source to `sources/config/sources.yaml` with: `name`, `url`, `license`, `attribution_text`, and any mapping fields (e.g. `translator`, `lang_code`).
3. Document the source in [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) with the exact attribution text users must preserve.
4. Extend `scripts/ingest.py` if needed to fetch and map the new source into the canonical schema.
5. Run `python scripts/ingest.py` and then `python scripts/validate.py` before committing.

## Attribution rules

- **Arabic text**: Must not be modified. Always attribute to Tanzil Project and link to https://tanzil.net/ (see [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md)).
- **Translations / transliteration / audio**: Each source must be listed in DATA_SOURCES.md with license and attribution text. Exports can include an attribution block via `--include-attribution`.

## Code and data quality

- Run the validator before submitting PRs that touch `data/` or the schema.
- Keep DATA_SOURCES.md and sources.yaml in sync when adding or changing sources.
