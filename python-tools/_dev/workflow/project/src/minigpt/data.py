from __future__ import annotations

from pathlib import Path

import numpy as np
import torch

from minigpt.clean import clean_text
from minigpt.tokenizer import CharTokenizer

def build_arrays(src="data/input.txt", out_dir="data", val_frac=0.1):
    """Clean, tokenize, split, and cache to .npy. Returns the tokenizer."""
    out = Path(out_dir)
    text = clean_text(Path(src).read_text(encoding="utf-8"))
    tok = CharTokenizer.from_text(text)
    ids = np.array(tok.encode(text), dtype=np.uint16)

    n = int(len(ids) * (1 - val_frac))
    np.save(out / "train.npy", ids[:n])
    np.save(out / "val.npy", ids[n:])
    tok.save(out / "vocab.json")
    print(f"vocab {tok.vocab_size} | train {n:,} | val {len(ids) - n:,}")
    return tok

def get_batch(split_array, block_size, batch_size, device, generator=None):
    """One batch of contexts x and their next-character targets y."""
    ix = torch.randint(len(split_array) - block_size - 1,
                       (batch_size,), generator=generator)
    data = torch.from_numpy(split_array.astype(np.int64))
    x = torch.stack([data[i:i + block_size] for i in ix])
    y = torch.stack([data[i + 1:i + block_size + 1] for i in ix])
    return x.to(device), y.to(device)
