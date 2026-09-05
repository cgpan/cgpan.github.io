from __future__ import annotations

import argparse

import torch

from minigpt.config import Config
from minigpt.model import GPT
from minigpt.tokenizer import CharTokenizer

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--temperature", type=float, default=0.8)
    ap.add_argument("--top-k", type=int, default=None)
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()
    if args.seed is not None:
        torch.manual_seed(args.seed)

    ck = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    cfg = Config(**ck["config"])
    tok = CharTokenizer.load("data/vocab.json")

    model = GPT(cfg)
    model.load_state_dict(ck["model"])
    model.to(cfg.device).eval()

    start = torch.zeros((1, 1), dtype=torch.long, device=cfg.device)
    out = model.generate(start, args.n, args.temperature, args.top_k)
    print(tok.decode(out[0].tolist()))

if __name__ == "__main__":
    main()
