# Contributing

The most valuable contribution is a native speaker's review. Generated packs are only as good as the checking they get.

## Ways to help

- **Remove or fix wrong pairs.** Edit the pack JSON (delete the pair) and open a pull request. Say in the description why; if a pair is wrong, also
  add it to `review/denylist.json` so it does not return when the pack is regenerated.
- **Review a whole pack.** If you are a native speaker and checked the entire pack, set `review.native_speaker_checked` to `true`, add
  `reviewed_by` (a name or handle) and a `note`. Do not set it for a partial check.
- **Add a language or vertical.** Open an issue first. New packs must follow [FORMAT.md](FORMAT.md) and pass `python scripts/validate.py`.

## Rules for pairs

- Real shop search vocabulary of the language; shoppers searching `a` should be happy to also see `b`.
- No brand names, model numbers, sizes or numbers.
- At most two words per term. Narrower or broader product types are not synonyms; leave them out.
- Terms must be folded as described in FORMAT.md; the validator checks this.

## Licensing of contributions

By contributing you agree that your contribution is licensed under [CC BY 4.0](LICENSE), like the rest of the repository.
