"""Print one training example so you can see that y is x shifted by one character."""
import numpy as np
import torch

from minigpt.data import get_batch
from minigpt.tokenizer import CharTokenizer

tok = CharTokenizer.load("data/vocab.json")
train = np.load("data/train.npy")
g = torch.Generator().manual_seed(0)
x, y = get_batch(train, block_size=8, batch_size=1, device="cpu", generator=g)
print("x:", repr(tok.decode(x[0])))
print("y:", repr(tok.decode(y[0])))
