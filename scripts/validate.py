#!/usr/bin/env python3
"""Validate every pack against format 1 (stdlib only): python scripts/validate.py"""
import glob
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SPECIAL = {"\u00df": "ss", "\u00e6": "ae", "\u0153": "oe", "\u00f8": "o", "\u0111": "d", "\u0142": "l", "\u0131": "i", "\u00fe": "th", "\u00f0": "d"}
SYMMETRIC = {"synonym", "variant", "abbreviation"}
TYPES = SYMMETRIC | {"misspelling", "broader"}


def fold(text):
    text = unicodedata.normalize("NFKC", text).lower().strip()
    for k, v in SPECIAL.items():
        text = text.replace(k, v)
    text = "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", text)


def check_pack(path, errors):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    try:
        pack = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors.append(f"{rel}: unreadable ({exc})")
        return 0
    lang, vertical = os.path.basename(os.path.dirname(path)), os.path.basename(path)[:-5]
    if pack.get("format") != 1:
        errors.append(f"{rel}: format must be 1")
    if pack.get("lang") != lang or pack.get("vertical") != vertical:
        errors.append(f"{rel}: lang/vertical do not match the path")
    if pack.get("license") != "CC-BY-4.0":
        errors.append(f"{rel}: license must be CC-BY-4.0")
    if not isinstance(pack.get("review", {}).get("native_speaker_checked"), bool):
        errors.append(f"{rel}: review.native_speaker_checked must be a boolean")
    seen = set()
    for i, p in enumerate(pack.get("pairs", [])):
        where = f"{rel} pair {i} ({p.get('a')!r}, {p.get('b')!r})"
        a, b, kind = p.get("a"), p.get("b"), p.get("type")
        if not isinstance(a, str) or not isinstance(b, str) or not a or not b:
            errors.append(f"{where}: a and b must be non-empty strings")
            continue
        if kind not in TYPES:
            errors.append(f"{where}: unknown type {kind!r}")
        if a == b:
            errors.append(f"{where}: a equals b")
        if fold(a) != a or fold(b) != b:
            errors.append(f"{where}: terms must be folded (lowercase, accent-free)")
        if len(a.split()) > 2 or len(b.split()) > 2:
            errors.append(f"{where}: more than two words")
        if kind in SYMMETRIC and (p.get("dir") != "both" or a > b):
            errors.append(f"{where}: symmetric pairs need dir 'both' and a sorted before b")
        if kind in ("misspelling", "broader") and p.get("dir") != "a>b":
            errors.append(f"{where}: directional pairs need dir 'a>b'")
        if not isinstance(p.get("conf"), (int, float)) or not 0 <= p["conf"] <= 1:
            errors.append(f"{where}: conf must be between 0 and 1")
        key = (a, b, kind)
        if key in seen:
            errors.append(f"{where}: duplicate pair")
        seen.add(key)
    return len(pack.get("pairs", []))


def main():
    errors = []
    counts = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "packs", "*", "*.json"))):
        counts[os.path.relpath(path, os.path.join(ROOT, "packs")).replace(os.sep, "/")] = check_pack(path, errors)
    index_path = os.path.join(ROOT, "packs", "index.json")
    try:
        index = json.load(open(index_path, encoding="utf-8"))
        listed = {e["file"]: e["pairs"] for e in index.get("packs", [])}
        if listed != counts:
            errors.append("packs/index.json does not match the pack files (files or pair counts differ)")
    except (OSError, ValueError, KeyError) as exc:
        errors.append(f"packs/index.json: {exc}")
    for e in errors[:50]:
        print("ERROR", e)
    print(f"{len(counts)} packs, {sum(counts.values())} pairs, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
