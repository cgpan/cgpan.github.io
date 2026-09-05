"""Score the counting bigram on the cached arrays: the number the transformer has to beat."""
import math

import numpy as np

from minigpt.baseline import CountBigram
from minigpt.tokenizer import CharTokenizer

tok = CharTokenizer.load("data/vocab.json")
train = np.load("data/train.npy")
val = np.load("data/val.npy")

untrained = CountBigram(tok.vocab_size)
print(f"uniform (untrained)   {untrained.nll(val):.4f}   = ln({tok.vocab_size})")

model = CountBigram(tok.vocab_size).fit(train)
val_loss = model.nll(val)
print(f"bigram, train         {model.nll(train):.4f}")
print(f"bigram, validation    {val_loss:.4f}   perplexity {math.exp(val_loss):.2f}")
