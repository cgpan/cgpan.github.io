"""Download tinyshakespeare into data/. Safe to re-run."""
import hashlib
import urllib.request
from pathlib import Path

URL = ("https://raw.githubusercontent.com/karpathy/char-rnn/"
       "master/data/tinyshakespeare/input.txt")
DEST = Path("data/input.txt")
EXPECTED_BYTES = 1_115_394

def main() -> None:
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if not DEST.exists():
        print(f"downloading -> {DEST}")
        urllib.request.urlretrieve(URL, DEST)
    raw = DEST.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()[:12]
    print(f"{len(raw):,} bytes  sha256:{digest}")
    if len(raw) != EXPECTED_BYTES:
        raise SystemExit("unexpected file size - the source may have changed")

if __name__ == "__main__":
    main()
