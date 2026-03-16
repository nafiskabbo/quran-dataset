#!/usr/bin/env python3
"""
Ingest Quran data from sources (see sources/config/sources.yaml) into data/quran.db.
Idempotent: replaces or upserts. Run with network access.
"""
from pathlib import Path
import json
import sys

import requests
import yaml

# Add scripts dir to path so we can import lib
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from lib.db import get_connection, get_db_path, get_data_dir
from lib.schema_loader import init_db


def load_sources_config() -> dict:
    config_path = REPO_ROOT / "sources" / "config" / "sources.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Sources config not found: {config_path}")
    return yaml.safe_load(config_path.read_text(encoding="utf-8"))


def fetch_json(url: str) -> dict:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.json()


def main() -> None:
    config = load_sources_config()
    print("Initializing database...")
    init_db()
    conn = get_connection()
    try:
        # 1. Surah metadata
        meta_url = config["surah_metadata"]["url"]
        print(f"Fetching surah metadata from {meta_url}...")
        resp = fetch_json(meta_url)
        surahs_data = resp.get("data") or []
        if not surahs_data:
            raise ValueError("No surah data in response")
        conn.executemany(
            """INSERT OR REPLACE INTO surahs (id, name_ar, name_en, translated_name, revelation_place, verse_count, "order")
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    s["number"],
                    s.get("name", ""),
                    s.get("englishName", ""),
                    s.get("englishNameTranslation"),
                    s.get("revelationType"),
                    s.get("numberOfAyahs", 0),
                    s["number"],
                )
                for s in surahs_data
            ],
        )
        conn.commit()
        print(f"  Inserted {len(surahs_data)} surahs.")
        print(f"  Attribution: {config['surah_metadata']['attribution_text'][:80]}...")

        # 2. Arabic verses (surah by surah to get juz, page)
        arabic_url_template = config["arabic"]["url"]
        # API full-quran might be one URL; we use per-surah for reliability and juz/page
        base = arabic_url_template.rsplit("/", 1)[0]  # e.g. https://api.alquran.cloud/v1/quran
        # Per-surah: https://api.alquran.cloud/v1/surah/1/quran-uthmani
        arabic_base = "https://api.alquran.cloud/v1/surah"
        verse_rows = []
        for surah_num in range(1, 115):
            url = f"{arabic_base}/{surah_num}/quran-uthmani"
            resp = fetch_json(url)
            data = resp.get("data") or {}
            ayahs = data.get("ayahs") or []
            for a in ayahs:
                verse_key = f"{surah_num}:{a.get('numberInSurah', a.get('number'))}"
                text = (a.get("text") or "").strip().replace("\ufeff", "")
                juz = a.get("juz")
                page = a.get("page")
                rub = a.get("hizbQuarter")
                sajdah = 1 if a.get("sajda") else None
                verse_rows.append(
                    (
                        surah_num,
                        a.get("numberInSurah", a.get("number")),
                        verse_key,
                        text,
                        None,  # text_simple
                        juz,
                        page,
                        rub,
                        sajdah,
                    )
                )
            if surah_num % 20 == 0:
                print(f"  Fetched Arabic verses for surahs 1-{surah_num}...")
        conn.executemany(
            """INSERT OR REPLACE INTO verses (surah_id, ayah_number, verse_key, text_uthmani, text_simple, juz, page, rub_el_hizb, sajdah)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            verse_rows,
        )
        conn.commit()
        print(f"  Inserted {len(verse_rows)} verses (Arabic).")
        print(f"  Attribution: {config['arabic']['attribution_text'][:80]}...")

        # 3. Translations (per-surah for reliability)
        for tr in config.get("translations", []):
            tid = tr.get("identifier", "")
            lang = tr.get("lang_code", "en")
            translator = tr.get("translator", "")
            print(f"Fetching translation {tid} ({translator})...")
            trans_rows = []
            for surah_num in range(1, 115):
                surah_url = f"https://api.alquran.cloud/v1/surah/{surah_num}/{tid}"
                try:
                    sr = fetch_json(surah_url)
                except Exception as e:
                    print(f"  Warning: failed translation {tid} for surah {surah_num}: {e}")
                    continue
                sd = sr.get("data") or {}
                ayahs = sd.get("ayahs") or []
                for a in ayahs:
                    num_in_surah = a.get("numberInSurah", a.get("number"))
                    verse_key = f"{surah_num}:{num_in_surah}"
                    trans_rows.append(
                        (
                            verse_key,
                            lang,
                            tid,
                            translator,
                            (a.get("text") or "").strip(),
                        )
                    )
                if surah_num % 30 == 0:
                    print(f"  Fetched translation {tid} for surahs 1-{surah_num}...")
            if trans_rows:
                conn.executemany(
                    "INSERT OR REPLACE INTO translations (verse_key, lang_code, edition_id, translator, text) VALUES (?, ?, ?, ?, ?)",
                    trans_rows,
                )
                conn.commit()
                print(f"  Inserted {len(trans_rows)} translation rows for {translator} ({lang}).")

        # 4. Transliteration (optional, single edition)
        translit_cfg = config.get("transliteration")
        if translit_cfg:
            tid = translit_cfg.get("identifier", "")
            lang = translit_cfg.get("lang_code", "en")
            print(f"Fetching transliteration {tid} (lang={lang})...")
            translit_rows = []
            for surah_num in range(1, 115):
                surah_url = f"https://api.alquran.cloud/v1/surah/{surah_num}/{tid}"
                try:
                    sr = fetch_json(surah_url)
                except Exception as e:
                    print(f"  Warning: failed transliteration {tid} for surah {surah_num}: {e}")
                    continue
                sd = sr.get("data") or {}
                ayahs = sd.get("ayahs") or []
                for a in ayahs:
                    num_in_surah = a.get("numberInSurah", a.get("number"))
                    verse_key = f"{surah_num}:{num_in_surah}"
                    translit_rows.append(
                        (
                            verse_key,
                            lang,
                            tid,
                            (a.get("text") or "").strip(),
                        )
                    )
                if surah_num % 30 == 0:
                    print(f"  Fetched transliteration {tid} for surahs 1-{surah_num}...")
            if translit_rows:
                conn.executemany(
                    "INSERT OR REPLACE INTO transliterations (verse_key, lang_code, edition_id, text) VALUES (?, ?, ?, ?)",
                    translit_rows,
                )
                conn.commit()
                print(f"  Inserted {len(translit_rows)} transliteration rows for lang={lang}.")

        # 5. Audio (optional, single reciter; verse-by-verse URLs)
        audio_cfg = config.get("audio")
        if audio_cfg:
            aid = audio_cfg.get("identifier", "")
            reciter_id = audio_cfg.get("reciter_id", aid or "default")
            print(f"Fetching audio recitation {aid} (reciter_id={reciter_id})...")
            audio_rows = []
            for surah_num in range(1, 115):
                surah_url = f"https://api.alquran.cloud/v1/surah/{surah_num}/{aid}"
                try:
                    sr = fetch_json(surah_url)
                except Exception as e:
                    print(f"  Warning: failed audio {aid} for surah {surah_num}: {e}")
                    continue
                sd = sr.get("data") or {}
                ayahs = sd.get("ayahs") or []
                for a in ayahs:
                    num_in_surah = a.get("numberInSurah", a.get("number"))
                    verse_key = f"{surah_num}:{num_in_surah}"
                    url = (a.get("audio") or "").strip()
                    if not url:
                        continue
                    audio_rows.append(
                        (
                            verse_key,
                            reciter_id,
                            url,
                            None,  # segment_url
                            None,  # duration_sec (not provided by API)
                            None,  # timestamp_start
                            None,  # timestamp_end
                        )
                    )
                if surah_num % 30 == 0:
                    print(f"  Fetched audio {aid} for surahs 1-{surah_num}...")
            if audio_rows:
                conn.executemany(
                    """
                    INSERT OR REPLACE INTO audio
                      (verse_key, reciter_id, url, segment_url, duration_sec, timestamp_start, timestamp_end)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    audio_rows,
                )
                conn.commit()
                print(f"  Inserted {len(audio_rows)} audio rows for reciter_id={reciter_id}.")

        # Optional: write surahs.json mirror
        data_dir = get_data_dir()
        data_dir.mkdir(parents=True, exist_ok=True)
        surahs_out = []
        for row in conn.execute("SELECT id, name_ar, name_en, translated_name, revelation_place, verse_count FROM surahs ORDER BY id"):
            surahs_out.append({
                "id": row[0],
                "name_ar": row[1],
                "name_en": row[2],
                "translated_name": row[3],
                "revelation_place": row[4],
                "verse_count": row[5],
            })
        (data_dir / "surahs.json").write_text(json.dumps(surahs_out, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Wrote data/surahs.json")

    finally:
        conn.close()
    print("Ingest complete.")


if __name__ == "__main__":
    main()
