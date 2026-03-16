## Translations and transliterations in this dataset

This dataset currently ingests a subset of the editions listed by the AlQuran Cloud API [`/v1/edition`](https://api.alquran.cloud/v1/edition). Each row below corresponds to an edition that is actually present in `data/quran.db`.

### Text translations

The `translations` table stores one row per verse per edition, with:

- `lang_code` — short language code used in this dataset (e.g. `en`, `bn`)
- `edition_id` — full edition identifier from AlQuran Cloud (e.g. `en.sahih`)
- `translator` — human‑readable translator / edition name

Current ingested editions:

| lang_code | edition_id     | translator / edition name                  |
|-----------|----------------|--------------------------------------------|
| en        | en.sahih       | Saheeh International                       |
| bn        | bn.bengali     | Muhiuddin Khan                             |
| ur        | ur.jalandhry   | Fateh Muhammad Jalandhry                   |
| fr        | fr.hamidullah  | Muhammad Hamidullah                        |
| id        | id.indonesian  | Bahasa Indonesia edition (id.indonesian)   |

To add more translations, extend `sources/config/sources.yaml` and re‑run `scripts/ingest.py`.

### Transliteration editions

The `transliterations` table stores one row per verse per transliteration edition, with:

- `lang_code` — short language code (e.g. `en`)
- `edition_id` — full edition identifier from AlQuran Cloud

Current ingested editions:

| lang_code | edition_id          | notes                |
|-----------|---------------------|----------------------|
| en        | en.transliteration  | English transliteration |

You can add more transliteration sources (subject to licensing) by updating `sources/config/sources.yaml` and re‑running `scripts/ingest.py`.

