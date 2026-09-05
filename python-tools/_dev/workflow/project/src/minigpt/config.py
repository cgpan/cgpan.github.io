from __future__ import annotations

from dataclasses import asdict, dataclass

import torch
import yaml

def get_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"

@dataclass
class Config:
    # model
    vocab_size: int = 65
    block_size: int = 256
    n_layer: int = 6
    n_head: int = 6
    n_embd: int = 384
    dropout: float = 0.2
    # optimisation
    batch_size: int = 64
    learning_rate: float = 3e-4
    max_iters: int = 5000
    eval_interval: int = 250
    eval_iters: int = 200
    # housekeeping
    seed: int = 1337
    device: str = ""

    def __post_init__(self):
        if self.n_embd % self.n_head != 0:
            raise ValueError("n_embd must be divisible by n_head")
        if not self.device:
            self.device = get_device()

    @classmethod
    def from_yaml(cls, path) -> "Config":
        with open(path) as f:
            return cls(**(yaml.safe_load(f) or {}))

    def to_dict(self) -> dict:
        return asdict(self)
