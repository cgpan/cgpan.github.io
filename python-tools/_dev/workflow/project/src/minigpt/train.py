from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from pathlib import Path

import numpy as np
import torch

from minigpt.config import Config
from minigpt.data import get_batch
from minigpt.model import GPT

def git_commit() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except Exception:
        return "unknown"

@torch.no_grad()
def estimate_loss(model, splits, cfg):
    """Average loss over many batches - one batch is far too noisy to steer by."""
    model.eval()
    out = {}
    for name, arr in splits.items():
        losses = torch.zeros(cfg.eval_iters)
        for k in range(cfg.eval_iters):
            x, y = get_batch(arr, cfg.block_size, cfg.batch_size, cfg.device)
            losses[k] = model(x, y)[1].item()
        out[name] = losses.mean().item()
    model.train()
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/base.yaml")
    ap.add_argument("--run-name", default=None)
    args = ap.parse_args()

    cfg = Config.from_yaml(args.config)
    torch.manual_seed(cfg.seed)
    np.random.seed(cfg.seed)

    run = args.run_name or time.strftime("%Y%m%d-%H%M%S")
    run_dir = Path("runs") / run
    run_dir.mkdir(parents=True, exist_ok=True)

    splits = {"train": np.load("data/train.npy"),
              "val": np.load("data/val.npy")}
    model = GPT(cfg).to(cfg.device)
    print(f"{model.n_params() / 1e6:.2f}M parameters on {cfg.device}")

    # the manifest ties every number you report to the exact code that made it
    (run_dir / "manifest.json").write_text(json.dumps(
        {"config": cfg.to_dict(), "commit": git_commit(),
         "params": model.n_params(), "started": run}, indent=2))

    opt = torch.optim.AdamW(model.parameters(), lr=cfg.learning_rate)
    log = open(run_dir / "log.csv", "w", newline="")
    writer = csv.writer(log)
    writer.writerow(["iter", "train_loss", "val_loss", "seconds"])

    best, t0 = float("inf"), time.time()
    for it in range(cfg.max_iters + 1):
        if it % cfg.eval_interval == 0 or it == cfg.max_iters:
            losses = estimate_loss(model, splits, cfg)
            dt = time.time() - t0
            print(f"iter {it:5d} | train {losses['train']:.4f} "
                  f"| val {losses['val']:.4f} | {dt:6.1f}s")
            writer.writerow([it, losses["train"], losses["val"], round(dt, 1)])
            log.flush()
            if losses["val"] < best:
                best = losses["val"]
                torch.save({"model": model.state_dict(),
                            "config": cfg.to_dict(), "iter": it, "val_loss": best},
                           run_dir / "best.pt")

        x, y = get_batch(splits["train"], cfg.block_size, cfg.batch_size, cfg.device)
        loss = model(x, y)[1]
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()

    log.close()
    print(f"best validation loss {best:.4f} -> {run_dir / 'best.pt'}")

if __name__ == "__main__":
    main()
