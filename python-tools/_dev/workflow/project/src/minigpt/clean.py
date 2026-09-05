"""Corpus cleaning: normalise whitespace and drop characters we will not model."""
from __future__ import annotations

import re
import unicodedata
from collections import Counter

SMART = {"‘": "'", "’": "'", "“": '"', "”": '"',
         "–": "-", "—": "--", "…": "..."}

def clean_text(raw: str, min_char_count: int = 0) -> str:
    text = unicodedata.normalize("NFKC", raw)
    for bad, good in SMART.items():
        text = text.replace(bad, good)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)      # runs of spaces -> one
    text = re.sub(r" *\n", "\n", text)       # trailing spaces on a line
    text = re.sub(r"\n{3,}", "\n\n", text)   # at most one blank line
    text = text.strip() + "\n"

    if min_char_count > 0:
        counts = Counter(text)
        rare = {ch for ch, n in counts.items() if n < min_char_count}
        text = "".join(ch for ch in text if ch not in rare)
    return text

def describe(text: str) -> dict:
    counts = Counter(text)
    return {"n_chars": len(text),
            "n_lines": text.count("\n") + 1,
            "vocab_size": len(counts),
            "most_common": counts.most_common(5)}
