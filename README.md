# Searchmaker Language Packs

Open synonym data for web-shop search, one pack per language and shop vertical. Made for the Searchmaker catalog engine and its WooCommerce
plugin, but plain JSON that any search system can use. 6,653 term pairs across 20 packs.

> **Status: machine-generated and not yet reviewed by native speakers.** Every pack says so in `review.native_speaker_checked`.
> Treat the data as a good starting point, not as ground truth. Corrections are welcome (see [CONTRIBUTING.md](CONTRIBUTING.md)).

## What is in here

| Language | Code | Packs | Pairs | Review status |
|---|---|---|---|---|
| Finnish | `fi` | 4 | 1,333 | generated, unreviewed |
| English | `en` | 4 | 1,503 | generated, unreviewed |
| Swedish | `sv` | 4 | 757 | generated, unreviewed |
| German | `de` | 4 | 1,886 | generated, unreviewed |
| Estonian | `et` | 4 | 1,174 | generated, unreviewed |

Verticals (one pack per language and vertical):

- `general`: general consumer and household products
- `tools`: power tools, hand tools, fasteners, workshop and construction supplies
- `garden`: garden, forestry and outdoor machinery and supplies
- `home`: furniture, home decor, kitchen and appliances

```text
packs/<lang>/<vertical>.json   the packs        packs/index.json   list of all packs
seeds/                         the seed words each pack was built from
review/                        pairs rejected in review (denylist) and the reviewers' notes
scripts/validate.py            checks packs against the format (run in CI)
```

A pack contains pairs like `{"a": "vatupassi", "b": "vesivaaka", "type": "synonym", "dir": "both"}`. Terms are lowercase and accent-folded the same way
the Searchmaker engine indexes text (`ä` becomes `a`), so a pack applies directly to indexed tokens. The full specification is in
[FORMAT.md](FORMAT.md).

Most pairs are one of three kinds: **synonyms** (`vatupassi` and `vesivaaka`), **variants** (compound split or join such as `jiiri saha` and
`jiirisaha`, spelling and inflection forms) and **abbreviations**. Misspellings are directional: searching the misspelling also finds the
correct term. Narrower or broader product terms are deliberately left out.

## How the packs were made

For each language and vertical, sub-categories and seed words were listed, a model proposed related search terms for every seed,
a second, separate pass judged each candidate pair strictly, and pairs failing the filters (model numbers, identical after folding,
too long, low agreement or confidence) were dropped. The Finnish packs additionally went through a review pass by a model;
the pairs it rejected are in `review/` and are never written to the packs (`review/denylist.json` also holds pairs rejected in earlier trial runs). The packs were generated with ChatGPT (OpenAI). The pipeline
records the model and prompt version in each pack's `generator` block.

No human has verified these lists. Expect a small share of wrong or too-broad pairs, especially among the synonyms (the compound variants
are far more reliable).

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE). You may use, modify and redistribute the data, including commercially,
if you give credit. Suggested credit line:

> Synonym data from Searchmaker Language Packs (searchmaker-language-packs), licensed CC BY 4.0.

Each pack carries `"license": "CC-BY-4.0"` so the notice travels with the file. The data comes with no warranty.

## Versioning

Releases are tagged `vMAJOR.MINOR.PATCH`. New languages or verticals bump the minor version, corrections the patch version, and a change of the
pack `format` the major version. Consumers should pin a tag and refuse packs whose `format` is newer than they understand.
