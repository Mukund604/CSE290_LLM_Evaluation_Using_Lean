#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

TACTIC_TOKENS = {
    "intro", "intros", "exact", "apply", "refine", "rfl", "simp",
    "simp_all", "simp_rw", "ring", "ring_nf", "norm_num", "linarith",
    "nlinarith", "polyrith", "omega", "decide", "aesop", "rcases",
    "obtain", "cases", "induction", "induction'", "rw", "rewrite",
    "have", "show", "change", "suffices", "calc", "by_contra",
    "push_neg", "exfalso", "contradiction", "constructor", "use",
    "left", "right", "fin_cases", "field_simp", "abel", "tauto",
    "trivial", "assumption", "linear_combination", "positivity",
    "interval_cases", "split_ifs", "subst", "rfl", "rwa",
}

TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9']*'?")
DOTTED_RE = re.compile(r"\b[A-Za-z_][A-Za-z_0-9']*"
                       r"(?:\.[A-Za-z_][A-Za-z_0-9']*)+")
HEAVY_CLOSERS = {"decide", "nlinarith", "polyrith", "omega", "aesop",
                 "norm_num", "linarith"}

def line_count(body: str) -> int:
    return sum(1 for ln in body.splitlines() if ln.strip())


def tactic_counts(body: str) -> Counter:
    return Counter(t for t in TOKEN_RE.findall(body) if t in TACTIC_TOKENS)


def lemma_idents(body: str) -> list[str]:
    return DOTTED_RE.findall(body)


def is_oneliner_close(body: str) -> bool:
    nonblank = [ln.strip() for ln in body.splitlines() if ln.strip()]
    if len(nonblank) != 1:
        return False
    return nonblank[0] in HEAVY_CLOSERS


def shape(row: dict) -> dict:
    body = row["proof"] or ""
    tc = tactic_counts(body)
    lemmas = lemma_idents(body)
    top3 = ", ".join(f"{t}={n}" for t, n in tc.most_common(3)) or "-"
    return {
        "problem": row["problem"],
        "lines": line_count(body),
        "tactic_total": sum(tc.values()),
        "tactic_top3": top3,
        "lemmas": len(lemmas),
        "lemmas_unique": len(set(lemmas)),
        "have_count": tc.get("have", 0),
        "calc_count": tc.get("calc", 0),
        "has_oneliner_close": is_oneliner_close(body),
    }


def load(path: Path) -> list[dict]:
    out: list[dict] = []
    for line in path.read_text().splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def md_table(rows: list[dict], cols: list[str]) -> str:
    if not rows:
        return "_(no rows)_\n"
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body_lines = ["| " + " | ".join(str(r.get(c, "")) for c in cols) + " |"
                  for r in rows]
    return "\n".join([header, sep, *body_lines]) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--human", type=Path,
                        default=Path("harness/results/human_baseline_input.jsonl"))
    parser.add_argument("--model", action="append", type=Path,
                        help="Model attempt JSONL (from generate.py). Repeatable.")
    parser.add_argument("--csv", type=Path,
                        help="Optional CSV output path.")
    parser.add_argument("--problems", action="append",
                        help="Restrict to these problem names.")
    args = parser.parse_args()

    if not args.human.exists() and not args.model:
        print("ERROR: at least --human or --model must point to data",
              file=sys.stderr)
        return 1

    flat: list[dict] = []

    if args.human.exists():
        for row in load(args.human):
            sh = shape(row)
            sh["source"] = "human"
            flat.append(sh)

    for mp in args.model or []:
        for row in load(mp):
            sh = shape(row)
            sh["source"] = f"{row.get('model','?')}/seed{row.get('seed','?')}"
            flat.append(sh)

    if args.problems:
        keep = set(args.problems)
        flat = [r for r in flat if r["problem"] in keep]

    if not flat:
        print("ERROR: no rows to compare", file=sys.stderr)
        return 1

    flat.sort(key=lambda r: (r["problem"], r["source"]))

    cols = ["problem", "source", "lines", "tactic_total", "tactic_top3",
            "lemmas", "lemmas_unique", "have_count", "calc_count",
            "has_oneliner_close"]
    sys.stdout.write("# Shape comparison\n\n")
    sys.stdout.write(md_table(flat, cols))

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in flat:
                w.writerow({c: r.get(c, "") for c in cols})
        print(f"\nWrote {args.csv}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
