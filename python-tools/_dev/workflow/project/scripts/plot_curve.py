"""Plot train and validation loss from a run's log.csv, with the two reference lines."""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

run = sys.argv[1] if len(sys.argv) > 1 else "runs/base"
df = pd.read_csv(f"{run}/log.csv")

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(df["iter"], df["train_loss"], label="train")
ax.plot(df["iter"], df["val_loss"], label="validation")
ax.axhline(2.4819, ls="--", lw=1, color="gray", label="counting bigram")
ax.axhline(4.1744, ls=":", lw=1, color="gray", label="untrained")
ax.set(xlabel="iteration", ylabel="cross-entropy (nats)")
ax.legend()
fig.tight_layout()
fig.savefig(f"{run}/curve.png", dpi=110)
print(f"saved {run}/curve.png")
