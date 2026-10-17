#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

from build_problems import SUBSET  # type: ignore

STRATUM_OF: dict[str, str] = {name: code for code, _, name, _ in SUBSET}

KEY_COLS = ("problem", "model", "seed", "condition")
HAND_COLS = ("hand_category", "root_cause", "near_miss", "notes")
HAND_CATEGORIES = (
    "hallucinated_lemma", "type_mismatch", "unfocused_goals",
    "near_miss_algebra", "wrong_strategy", "lean3_4_confusion",
    "heavy_tactic_misuse", "syntax_error", "partial_proof", "other",
)

def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()
            if line.strip()]


def key_of(row: dict) -> tuple:
    return tuple(row.get(k) for k in KEY_COLS)


def stratified_sample(rows: list[dict], n: int,
                      seed: int = 0) -> list[dict]:
    rng = random.Random(seed)
    buckets: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        buckets[(r["model"], r.get("_stratum", "?"),
                 r.get("category", "other"))].append(r)
    total = sum(len(v) for v in buckets.values())
    if total == 0:
        return []

    quotas = {k: max(1, math.floor(n * len(v) / total))
              for k, v in buckets.items()}
    picked: list[dict] = []
    for k, group in buckets.items():
        q = min(quotas[k], len(group))
        picked.extend(rng.sample(group, q))

    if len(picked) < n:
        remaining = [r for r in rows if r not in picked]
        topup = rng.sample(remaining, min(n - len(picked), len(remaining)))
        picked.extend(topup)

    return picked


def cmd_sample(args: argparse.Namespace) -> int:
    results: list[dict] = []
    for p in args.results:
        results.extend(load_jsonl(p))
    attempts: dict[tuple, dict] = {}
    for p in args.attempts:
        for r in load_jsonl(p):
            attempts[key_of(r)] = r

    failures: list[dict] = []
    for r in results:
        if r.get("passed"):
            continue
        att = attempts.get(key_of(r), {})
        r["_stratum"] = STRATUM_OF.get(r["problem"], "?")
        r["_proof"] = att.get("proof", "")
        r["_raw_response"] = att.get("raw_response", "")
        failures.append(r)

    if not failures:
        print("No failed rows found.", file=sys.stderr)
        return 1

    sampled = stratified_sample(failures, args.n, seed=args.seed)
    sampled.sort(key=lambda r: (r["model"], r["_stratum"],
                                r.get("category", "other"), r["problem"],
                                r.get("seed", 0)))

    cols = [
        "problem", "stratum", "model", "seed", "condition",
        "auto_category", "duration_s", "stderr_excerpt", "proof",
        *HAND_COLS,
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in sampled:
            w.writerow({
                "problem": r["problem"],
                "stratum": r["_stratum"],
                "model": r["model"],
                "seed": r.get("seed"),
                "condition": r.get("condition", "baseline"),
                "auto_category": r.get("category", "other"),
                "duration_s": r.get("duration_s", ""),
                "stderr_excerpt": r.get("stderr_excerpt", ""),
                "proof": r.get("_proof", ""),
                **{c: "" for c in HAND_COLS},
            })

    print(f"Sampled {len(sampled)} failures across "
          f"{len({(r['model'], r['_stratum'], r.get('category','other')) for r in sampled})}"
          f" (model, stratum, category) buckets",
          file=sys.stderr)
    print(f"Allowed hand_category values: {', '.join(HAND_CATEGORIES)}",
          file=sys.stderr)
    print(f"Wrote {args.out}", file=sys.stderr)
    return 0


def cmd_merge(args: argparse.Namespace) -> int:
    codes: dict[tuple, dict] = {}
    with args.csv.open() as f:
        for row in csv.DictReader(f):
            key = (row["problem"], row["model"],
                   int(row["seed"]) if row.get("seed") else 0,
                   row.get("condition", "baseline"))
            codes[key] = {c: row.get(c, "") for c in HAND_COLS}

    bad = [v["hand_category"] for v in codes.values()
           if v["hand_category"]
           and v["hand_category"] not in HAND_CATEGORIES]
    if bad:
        print(f"WARN: {len(bad)} rows have hand_category outside the "
              f"controlled vocabulary: {sorted(set(bad))}", file=sys.stderr)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for p in args.results:
        rows = load_jsonl(p)
        for r in rows:
            extra = codes.get(key_of(r))
            if extra:
                r.update(extra)
        out = args.out_dir / p.name
        with out.open("w") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
    coded = sum(1 for k in codes if codes[k].get("hand_category"))
    print(f"Merged {coded} hand-coded rows into "
          f"{len(args.results)} result files under {args.out_dir}/",
          file=sys.stderr)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="mode", required=True)

    p_sample = sub.add_parser("sample", help="Sample failures into a CSV.")
    p_sample.add_argument("--results", nargs="+", type=Path, required=True)
    p_sample.add_argument("--attempts", nargs="+", type=Path, required=True)
    p_sample.add_argument("--n", type=int, default=80)
    p_sample.add_argument("--seed", type=int, default=0)
    p_sample.add_argument("--out", type=Path, required=True)
    p_sample.set_defaults(func=cmd_sample)

    p_merge = sub.add_parser("merge", help="Merge codes back into result JSONLs.")
    p_merge.add_argument("--csv", type=Path, required=True)
    p_merge.add_argument("--results", nargs="+", type=Path, required=True)
    p_merge.add_argument("--out-dir", type=Path, required=True)
    p_merge.set_defaults(func=cmd_merge)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
