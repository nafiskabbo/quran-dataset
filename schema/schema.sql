-- Canonical schema for quran-dataset
-- Standard: 114 surahs, 6236 verses (Hafs), 30 juz, 604 pages

-- Surahs (chapters)
CREATE TABLE IF NOT EXISTS surahs (
  id INTEGER PRIMARY KEY CHECK (id >= 1 AND id <= 114),
  name_ar TEXT NOT NULL,
  name_en TEXT NOT NULL,
  translated_name TEXT,
  revelation_place TEXT,
  verse_count INTEGER NOT NULL,
  "order" INTEGER
);

CREATE INDEX IF NOT EXISTS idx_surahs_order ON surahs("order");

-- Verses (Arabic text + metadata)
CREATE TABLE IF NOT EXISTS verses (
  surah_id INTEGER NOT NULL REFERENCES surahs(id),
  ayah_number INTEGER NOT NULL,
  verse_key TEXT NOT NULL UNIQUE,
  text_uthmani TEXT NOT NULL,
  text_simple TEXT,
  juz INTEGER,
  page INTEGER,
  rub_el_hizb INTEGER,
  sajdah INTEGER,
  PRIMARY KEY (surah_id, ayah_number)
);

CREATE INDEX IF NOT EXISTS idx_verses_verse_key ON verses(verse_key);
CREATE INDEX IF NOT EXISTS idx_verses_surah_id ON verses(surah_id);
CREATE INDEX IF NOT EXISTS idx_verses_juz ON verses(juz);
CREATE INDEX IF NOT EXISTS idx_verses_page ON verses(page);

-- Translations (one row per verse per edition)
CREATE TABLE IF NOT EXISTS translations (
  verse_key TEXT NOT NULL,
  lang_code TEXT NOT NULL,
  edition_id TEXT NOT NULL,
  translator TEXT NOT NULL,
  text TEXT NOT NULL,
  FOREIGN KEY (verse_key) REFERENCES verses(verse_key)
);

CREATE INDEX IF NOT EXISTS idx_translations_verse_key ON translations(verse_key);
CREATE INDEX IF NOT EXISTS idx_translations_lang ON translations(lang_code);
CREATE INDEX IF NOT EXISTS idx_translations_edition ON translations(edition_id);

-- Transliterations (e.g. English/Latin)
CREATE TABLE IF NOT EXISTS transliterations (
  verse_key TEXT NOT NULL,
  lang_code TEXT NOT NULL,
  edition_id TEXT NOT NULL,
  text TEXT NOT NULL,
  FOREIGN KEY (verse_key) REFERENCES verses(verse_key)
);

CREATE INDEX IF NOT EXISTS idx_transliterations_verse_key ON transliterations(verse_key);
CREATE INDEX IF NOT EXISTS idx_transliterations_lang ON transliterations(lang_code);

-- Audio (URLs or segment metadata per reciter)
CREATE TABLE IF NOT EXISTS audio (
  verse_key TEXT NOT NULL,
  reciter_id TEXT NOT NULL,
  url TEXT,
  segment_url TEXT,
  duration_sec REAL,
  timestamp_start REAL,
  timestamp_end REAL,
  FOREIGN KEY (verse_key) REFERENCES verses(verse_key)
);

CREATE INDEX IF NOT EXISTS idx_audio_verse_key ON audio(verse_key);
CREATE INDEX IF NOT EXISTS idx_audio_reciter ON audio(reciter_id);

-- Optional: dataset/schema version for traceability
CREATE TABLE IF NOT EXISTS meta (
  key TEXT PRIMARY KEY,
  value TEXT
);

INSERT OR IGNORE INTO meta (key, value) VALUES ('schema_version', '1');
INSERT OR IGNORE INTO meta (key, value) VALUES ('dataset_version', '1.0.0');
