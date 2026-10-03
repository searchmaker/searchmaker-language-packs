# Pack format 1

## `packs/<lang>/<vertical>.json`

```json
{
  "format": 1,
  "lang": "fi",
  "vertical": "tools",
  "version": "2026-10-03",
  "license": "CC-BY-4.0",
  "source": "searchmaker-language-packs",
  "generator": { "models": ["chatgpt"], "prompt_version": ["2"], "passes": 1,
                 "thresholds": { "min_agreement": 0.66, "min_conf": 0.6, "min_critic": 0.67 }, "critic": true },
  "review": { "native_speaker_checked": false, "note": "..." },
  "dropped": { "critic": 10, "broader": 6 },
  "pairs": [ { "a": "vatupassi", "b": "vesivaaka", "type": "synonym", "dir": "both", "conf": 1.0, "votes": 1, "critic": 1.0 } ]
}
```

| Field | Meaning |
|---|---|
| `format` | Pack format version. Consumers must refuse a number they do not know. |
| `lang`, `vertical` | ISO 639-1 style language code and the shop area; they match the folder and file name. |
| `version` | Date the pack was built. |
| `generator` | How it was made: models, prompt version, number of samples per seed, filter thresholds, whether a critic pass ran. |
| `review` | `native_speaker_checked` is `true` only after a native speaker reviewed the pack; `reviewed_by` and `note` say who or what reviewed it. |
| `dropped` | How many candidate pairs each filter removed (informational). |
| `pairs` | The data, sorted by `conf` descending. |

## Pairs

| Key | Meaning |
|---|---|
| `a`, `b` | The two terms: one or two words, lowercase, accent-folded (see below). |
| `type` | `synonym`, `variant`, `abbreviation` or `misspelling`. |
| `dir` | `both`: searching either term should also find the other. `a>b`: searching `a` should also find `b`, not the reverse. |
| `conf` | Score 0 to 1 combining agreement between samples, the model's confidence, and whether the pair was proposed from both sides. |
| `votes` | How many samples proposed the pair. |
| `critic` | Share of strict second-pass judgements that approved the pair (present when a critic pass ran). |

Rules by type: `synonym`, `variant` and `abbreviation` pairs are symmetric (`dir: both`) and stored with `a` sorted before `b`.
`misspelling` pairs are directional: `a` is the misspelling, `b` the correct term (`dir: a>b`).
A `broader` type (`a` is a narrower product type than `b`, `dir: a>b`) is part of the format but no published pack contains it.

## Term folding

Terms are normalized like this (identical to the Searchmaker engine): Unicode NFKC, lowercase, trim, replace
`ß→ss æ→ae œ→oe ø→o đ→d ł→l ı→i þ→th ð→d`, decompose (NFD) and drop combining marks (`ä→a`, `š→s`, `õ→o`), collapse whitespace.
Hyphens and spaces inside a term are kept; multi-word terms are matched on their tokens.

## `packs/index.json`

```json
{ "format": 1, "license": "CC-BY-4.0",
  "packs": [ { "lang": "fi", "vertical": "tools", "file": "fi/tools.json", "pairs": 363, "version": "2026-10-03",
               "native_speaker_checked": false, "reviewed_by": "ChatGPT" } ] }
```

## `review/denylist.json`

Pairs rejected in review: `{ "lang", "vertical", "a", "b", "type", "by" }`. Pack builders skip them, so they do not come back when a pack is regenerated.
