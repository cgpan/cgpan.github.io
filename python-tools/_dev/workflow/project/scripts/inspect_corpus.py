"""Print what cleaning did to the corpus: size, vocabulary, and the most common characters."""
from pathlib import Path

from minigpt.clean import clean_text, describe

raw = Path("data/input.txt").read_text(encoding="utf-8")
text = clean_text(raw)
r, c = describe(raw), describe(text)
print(f"raw:    {r['n_chars']:,} chars   vocab {r['vocab_size']}")
print(f"clean:  {c['n_chars']:,} chars   vocab {c['vocab_size']}   lines {c['n_lines']:,}")
print("most common:", " | ".join(f"{ch!r} {n:,}" for ch, n in c["most_common"]))
