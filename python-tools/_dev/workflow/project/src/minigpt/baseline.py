"""Count-based bigram model. The number the transformer has to beat."""
from __future__ import annotations

import numpy as np

class CountBigram:
    def __init__(self, vocab_size: int, alpha: float = 1.0):
        self.vocab_size = vocab_size
        self.alpha = alpha                       # add-alpha smoothing
        self.counts = np.zeros((vocab_size, vocab_size), dtype=np.float64)

    def fit(self, ids) -> "CountBigram":
        ids = np.asarray(ids)
        np.add.at(self.counts, (ids[:-1], ids[1:]), 1.0)
        return self

    @property
    def probs(self) -> np.ndarray:
        smoothed = self.counts + self.alpha
        return smoothed / smoothed.sum(axis=1, keepdims=True)

    def nll(self, ids) -> float:
        """Mean negative log likelihood in nats - same units as cross_entropy."""
        ids = np.asarray(ids)
        p = self.probs[ids[:-1], ids[1:]]
        return float(-np.log(p).mean())

    def generate(self, n: int, start: int = 0, seed: int = 0) -> list[int]:
        rng = np.random.default_rng(seed)
        probs, out, cur = self.probs, [start], start
        for _ in range(n):
            cur = int(rng.choice(self.vocab_size, p=probs[cur]))
            out.append(cur)
        return out
