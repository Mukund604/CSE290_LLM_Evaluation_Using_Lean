#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate  # noqa: E402

PERTURB_ROOT = Path("harness/problems_perturbed")


THEOREM_RE = re.compile(
    r"^(theorem\s+\S+.*?)\s*:=\s*by\s*$\n(\s*sorry)?",
    re.MULTILINE | re.DOTALL,
)


def parse_perturbed_lean(path: Path) -> tuple[str, str]:
    text = path.read_text()
    m = THEOREM_RE.search(text)
    if not m:
        raise ValueError(f"no theorem block in {path}")
    formal_full = m.group(1)
    header_end = text.find(formal_full)
    header = text[:header_end]
    formal_statement = formal_full + " := by\n"
    return header, formal_statement


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider",
                        choices=generate.CALLERS.keys(), required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--kind", required=True,
                        choices=("alpha_rename", "hyp_reorder", "restate"))
    parser.add_argument("--problem", action="append",
                        help="Problem name (repeatable). Defaults to all "
                             "perturbed templates available for --kind.")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--condition", default="baseline",
                        choices=sorted(generate.CONDITION_PROMPTS))
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--max-tokens", type=int, default=32768)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    load_dotenv()

    kind_dir = PERTURB_ROOT / args.kind
    if not kind_dir.exists():
        sys.exit(f"ERROR: no perturbed templates at {kind_dir}")

    if args.problem:
        names = args.problem
    else:
        names = sorted(p.stem for p in kind_dir.glob("*.lean"))

    missing = [n for n in names
               if not (kind_dir / f"{n}.lean").exists()]
    if missing:
        sys.exit(f"ERROR: no perturbed templates for {missing} under {kind_dir}")

    caller = generate.CALLERS[args.provider]
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("w") as out:
        for name in names:
            header, formal = parse_perturbed_lean(kind_dir / f"{name}.lean")
            problem = {"name": name, "header": header,
                       "formal_statement": formal}
            start = time.monotonic()
            try:
                raw = caller(args.model, problem,
                             args.temperature, args.max_tokens,
                             args.condition)
            except Exception as e:
                raw = ""
                err = f"{type(e).__name__}: {e}"
                print(f"  {name} ERROR {err}", file=sys.stderr)
            else:
                err = ""
            proof = generate.extract_proof(raw)
            row = {
                "problem": name,
                "proof": proof,
                "model": args.model,
                "seed": args.seed,
                "condition": args.condition,
                "perturbation": args.kind,
                "raw_response": raw,
                "elapsed_s": round(time.monotonic() - start, 2),
                "error": err,
            }
            out.write(json.dumps(row) + "\n")
            out.flush()
            status = "ERR" if err else f"{len(proof.splitlines())} lines"
            print(f"  {name} ({row['elapsed_s']}s, {status})",
                  file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
