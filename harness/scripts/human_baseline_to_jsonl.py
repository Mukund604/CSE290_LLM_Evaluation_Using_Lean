#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

SPLIT_RE = re.compile(r":=\s*by\s*\n", re.MULTILINE)
AUTHOR_RE = re.compile(r"^--\s*Author:\s*(.+?)\s*$", re.MULTILINE)

def extract(path: Path) -> dict | None:
    text = path.read_text()
    name = path.stem
    parts = SPLIT_RE.split(text)
    if len(parts) < 2:
        return None
    proof = parts[-1].rstrip()
    lines = proof.splitlines()
    indents = [len(l) - len(l.lstrip(" ")) for l in lines if l.strip()]
    dedent = min(indents) if indents else 0
    lines = [(l[dedent:] if l.strip() else "") for l in lines]
    proof = "\n".join(lines)

    author = ""
    m = AUTHOR_RE.search(text)
    if m:
        author = m.group(1)
        if author.startswith("(") and author.endswith(")"):
            author = ""

    return {
        "problem": name, "proof": proof,
        "model": "human", "seed": 0, "condition": "human_baseline",
        "author": author,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--in-dir", type=Path,
                        default=Path("human_baseline/problems"))
    parser.add_argument("--output", type=Path,
                        default=Path("harness/results/human_baseline_input.jsonl"))
    args = parser.parse_args()

    rows: list[dict] = []
    for path in sorted(args.in_dir.glob("*.lean")):
        row = extract(path)
        if row is None:
            print(f"WARN: {path.name} has no `:= by` block, skipping",
                  file=sys.stderr)
            continue
        rows.append(row)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    n_filled = sum(1 for r in rows if r["proof"].strip()
                   and r["proof"].strip() != "sorry")
    print(f"Wrote {len(rows)} rows to {args.output} "
          f"({n_filled} non-placeholder proofs)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())