"""Character-level tokenizer: text <-> list[int]."""
from __future__ import annotations

import json
from pathlib import Path

class CharTokenizer:
    def __init__(self, chars: list[str]):
        if len(set(chars)) != len(chars):
            raise ValueError("vocabulary contains duplicate characters")
        self.chars = list(chars)
        self.stoi = {ch: i for i, ch in enumerate(self.chars)}
        self.itos = {i: ch for i, ch in enumerate(self.chars)}

    @classmethod
    def from_text(cls, text: str) -> "CharTokenizer":
        return cls(sorted(set(text)))

    @property
    def vocab_size(self) -> int:
        return len(self.chars)

    def encode(self, text: str) -> list[int]:
        try:
            return [self.stoi[ch] for ch in text]
        except KeyError as e:
            raise ValueError(f"character {e.args[0]!r} not in vocabulary") from None

    def decode(self, ids) -> str:
        return "".join(self.itos[int(i)] for i in ids)

    def save(self, path) -> None:
        Path(path).write_text(json.dumps({"chars": self.chars}), encoding="utf-8")

    @classmethod
    def load(cls, path) -> "CharTokenizer":
        return cls(json.loads(Path(path).read_text(encoding="utf-8"))["chars"])
