#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import ssl
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO = "roozbeh-yz/miniF2F_v2"
DEFAULT_COMMIT = "main"
FILES = ["datasets/miniF2F_v2c.json", "datasets/miniF2F_v2s.json"]

def _download(url: str) -> bytes:
    try:
        with urllib.request.urlopen(url) as r:
            return r.read()
    except (urllib.error.URLError, ssl.SSLError) as e:
        print(f"  urllib failed ({e}); falling back to curl", file=sys.stderr)
        out = subprocess.run(["curl", "-fsSL", url], capture_output=True, check=True)
        return out.stdout


def fetch(commit: str, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for relpath in FILES:
        url = f"https://raw.githubusercontent.com/{REPO}/{commit}/{relpath}"
        dest = out_dir / Path(relpath).name
        print(f"Fetching {url} -> {dest}")
        data = _download(url)
        json.loads(data)
        dest.write_bytes(data)
    (out_dir / "_FETCHED_COMMIT").write_text(commit + "\n")
    print(f"Done. Pinned commit recorded in {out_dir / '_FETCHED_COMMIT'}.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", default=DEFAULT_COMMIT,
                        help="Upstream git ref (default: main).")
    parser.add_argument("--out", default="datasets",
                        help="Output directory (default: ./datasets).")
    args = parser.parse_args()
    fetch(args.commit, Path(args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
