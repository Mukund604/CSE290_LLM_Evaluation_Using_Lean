#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from parse_errors import classify, is_pass

SORRY_RE = re.compile(r"^\s*sorry\s*$", re.MULTILINE)

def substitute_proof(template_text: str, proof: str) -> str:
    indented = "\n".join(
        ("  " + line) if line.strip() else line for line in proof.splitlines()
    )
    new_text, n = SORRY_RE.subn(indented, template_text, count=1)
    if n == 0:
        raise ValueError("template did not contain a `sorry` placeholder")
    return new_text


def verify_one(row: dict, problems_dir: Path, timeout: float) -> dict:
    name = row["problem"]
    template = problems_dir / f"{name}.lean"
    if not template.exists():
        return {**row, "passed": False, "duration_s": 0.0,
                "category": "missing_template",
                "stderr_excerpt": f"no template at {template}"}

    text = substitute_proof(template.read_text(), row["proof"])
    with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False) as f:
        f.write(text)
        tmp_path = Path(f.name)

    start = time.monotonic()
    try:
        proc = subprocess.run(
            ["lake", "env", "lean", str(tmp_path)],
            capture_output=True, text=True, timeout=timeout,
        )
        diagnostics = (proc.stdout or "") + (proc.stderr or "")
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        diagnostics = "__HARNESS_TIMEOUT__"
        rc = -1
    finally:
        duration = time.monotonic() - start
        tmp_path.unlink(missing_ok=True)

    passed = is_pass(diagnostics, rc)
    cls = classify(diagnostics)
    return {
        "problem": name,
        "model": row.get("model"),
        "seed": row.get("seed"),
        "condition": row.get("condition", "baseline"),
        "passed": passed,
        "duration_s": round(duration, 2),
        "category": "passed" if passed else cls.category,
        "stderr_excerpt": "" if passed else cls.matched_excerpt,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path,
                        help="Input JSONL (default: stdin).")
    parser.add_argument("--output", type=Path,
                        help="Output JSONL (default: stdout).")
    parser.add_argument("--problems-dir", type=Path,
                        default=Path("harness/problems"))
    parser.add_argument("--timeout", type=float, default=180.0,
                        help="Per-problem timeout in seconds (default: 180).")
    parser.add_argument("--jobs", type=int, default=4,
                        help="Parallel verifications (default: 4).")
    args = parser.parse_args()

    in_stream = args.input.open() if args.input else sys.stdin
    out_stream = args.output.open("w") if args.output else sys.stdout
    rows = [json.loads(line) for line in in_stream if line.strip()]

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(verify_one, r, args.problems_dir, args.timeout)
                   for r in rows]
        for fut in as_completed(futures):
            result = fut.result()
            out_stream.write(json.dumps(result) + "\n")
            out_stream.flush()

    return 0


if __name__ == "__main__":
    sys.exit(main())
