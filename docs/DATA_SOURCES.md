# Data sources and attribution

This document lists every source used in the quran-dataset and the attribution you must preserve when using or redistributing the data.

## Arabic (Uthmani) text

- **Source:** Tanzil Project
- **URL:** https://tanzil.net/download
- **License:** Creative Commons Attribution 3.0 (CC BY 3.0)
- **Terms:** Verbatim copy and distribution allowed; **changing the text is not allowed**. Source must be clearly indicated with a link to tanzil.net.
- **Updates:** http://tanzil.net/updates/

**Attribution text (include in derivatives):**

```
Arabic Quran text: Tanzil Quran Text
Copyright (C) 2007-2021 Tanzil Project
License: Creative Commons Attribution 3.0
Source: https://tanzil.net/
This text may not be modified. See https://tanzil.net/docs/Text_License
```

---

## Translations

Each translation edition is listed below. Use only editions with clear open licenses and always credit the translator and the distribution source.

### Tanzil translations

- **URL:** https://tanzil.net/trans/
- **Note:** Multiple languages; check each edition’s license on the site.

**Example (English – Saheeh International):**  
"Translation by Saheeh International. Source: Tanzil (https://tanzil.net/trans/)."  
State the license indicated by Tanzil for that edition in your documentation.

If you use data from **Quran JSON API** (https://quran-json-api.vercel.app/data-sources): that project uses **CC-BY-SA 4.0**. You must comply with CC-BY-SA 4.0 and attribute both the API and the original translators (e.g. Russian by Elmir Kuliev, French by Muhammad Hamidullah, English by Saheeh International, etc.).

**In this repo:** Each translation source is defined in `sources/config/sources.yaml` with `name`, `url`, `license`, `attribution_text`, and `translator` (or edition id). Keep DATA_SOURCES.md and sources.yaml in sync when adding sources.

---

## Transliteration (e.g. English / Latin)

- **Source:** Tanzil Project
- **URL:** https://tanzil.net
- **License:** Creative Commons Attribution 3.0 (CC BY 3.0)
- **Attribution:** "Transliteration: Tanzil Project (https://tanzil.net). License: CC BY 3.0."

---

## Metadata (surah names, juz, page, revelation place)

- **Source:** Tanzil Quran Metadata
- **URL:** https://tanzil.net/docs/Quran_Metadata
- **Attribution:** "Quran metadata (surah names, juz, page): Tanzil Project, https://tanzil.net/docs/Quran_Metadata"

---

## Audio (if included)

Any audio source must be listed here with:

- Provider / reciter name
- URL
- License or terms of use
- Exact attribution text

Example format: "Audio: [Reciter name]. Source: [URL]. [License/terms]."

---

## Summary for users

When you use or redistribute data from this dataset:

1. **Do not modify** the Arabic Quran text.
2. **Include** the attribution text above for each type of data you use (Arabic, translations, transliteration, metadata, audio).
3. **Link** to this file or to the original sources (tanzil.net, etc.) so users can track updates.
4. For exports, you can use `python scripts/export.py --include-attribution` to append a short attribution block to the output.
