# Canonical schema

The dataset is stored in SQLite (`data/quran.db`). Table definitions live in `schema/schema.sql`.

## Standard counts

- **Surahs:** 114
- **Verses:** 6,236 (Hafs numbering)
- **Juz:** 30
- **Pages (Mushaf):** 604

## Tables

### surahs

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| id | INTEGER | Yes | 1–114, primary key |
| name_ar | TEXT | Yes | Arabic name |
| name_en | TEXT | Yes | English name |
| translated_name | TEXT | No | Optional translated name |
| revelation_place | TEXT | No | Meccan / Medinan |
| verse_count | INTEGER | Yes | Number of verses in surah |
| order | INTEGER | No | Display order (default = id) |

### verses

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| surah_id | INTEGER | Yes | FK to surahs.id |
| ayah_number | INTEGER | Yes | Verse number within surah |
| verse_key | TEXT | Yes | e.g. "1:1", unique |
| text_uthmani | TEXT | Yes | Arabic Uthmani script |
| text_simple | TEXT | No | Simplified Arabic (optional) |
| juz | INTEGER | No | 1–30 |
| page | INTEGER | No | Mushaf page 1–604 |
| rub_el_hizb | INTEGER | No | Quarter-hizb |
| sajdah | INTEGER | No | Sajdah verse marker (optional) |

Indexes: `verse_key`, `surah_id`.

### translations

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| verse_key | TEXT | Yes | e.g. "1:1", matches verses.verse_key |
| lang_code | TEXT | Yes | e.g. "en" |
| translator | TEXT | Yes | Edition / translator name |
| text | TEXT | Yes | Translation text |

Indexes: `verse_key`, `lang_code`.

### transliterations

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| verse_key | TEXT | Yes | e.g. "1:1" |
| lang_code | TEXT | Yes | e.g. "en" |
| text | TEXT | Yes | Transliteration text |

### audio

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| verse_key | TEXT | Yes | e.g. "1:1" |
| reciter_id | TEXT | Yes | Reciter identifier |
| url | TEXT | No | Single audio URL |
| segment_url | TEXT | No | Per-verse or segment URL pattern |
| duration_sec | REAL | No | Duration in seconds |
| timestamp_start | REAL | No | Start time (for segments) |
| timestamp_end | REAL | No | End time (for segments) |

## Joins

- Verses ↔ surahs: `verses.surah_id = surahs.id`
- Translations / transliterations / audio ↔ verses: `verse_key` (e.g. `translations.verse_key = verses.verse_key`)

## Optional tables (future)

- **tafsir:** verse_key, source, text or reference
- **words:** word-by-word Arabic and transliteration per verse
