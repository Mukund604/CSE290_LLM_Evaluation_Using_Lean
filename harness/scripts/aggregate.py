#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

from build_problems import SUBSET  # type: ignore

STRATUM_OF: dict[str, str] = {name: code for code, _, name, _ in SUBSET}
STRATUM_LABEL: dict[str, str] = {code: label for code, label, _, _ in SUBSET}
STRATA_ORDER = sorted({code for code, _, _, _ in SUBSET})

def load_rows(paths: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for p in paths:
        for line in p.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            r["_source"] = str(p)
            r.setdefault("condition", "baseline")
            r["_stratum"] = STRATUM_OF.get(r["problem"], "?")
            rows.append(r)
    return rows


def pool_pass_rates(rows: list[dict]) -> tuple[float, float, int]:
    by_problem: dict[str, list[bool]] = defaultdict(list)
    by_problem_per_ms: dict[str, dict[tuple[str, int], bool]] = defaultdict(dict)
    for r in rows:
        by_problem[r["problem"]].append(bool(r["passed"]))
        key = (r["model"], r["seed"])
        by_problem_per_ms[r["problem"]][key] = (
            by_problem_per_ms[r["problem"]].get(key, False) or bool(r["passed"])
        )
    if not by_problem:
        return 0.0, 0.0, 0
    union = statistics.mean(any(v) for v in by_problem.values())
    intersection = statistics.mean(
        all(per_ms.values()) for per_ms in by_problem_per_ms.values()
    )
    return union, intersection, len(by_problem)


def by_keys(rows: list[dict], keys: tuple[str, ...]) -> dict[tuple, list[dict]]:
    out: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        out[tuple(r.get(k) for k in keys)].append(r)
    return out


def pass_rate(rows: list[dict]) -> float:
    return statistics.mean(bool(r["passed"]) for r in rows) if rows else 0.0


def per_model_condition(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    for (model, cond), group in sorted(by_keys(rows, ("model", "condition")).items()):
        seed_rates = []
        for (_m, _c, _seed), srows in sorted(
                by_keys(group, ("model", "condition", "seed")).items()):
            seed_rates.append(pass_rate(srows))
        out.append({
            "model": model, "condition": cond,
            "n_rows": len(group),
            "n_problems": len({r["problem"] for r in group}),
            "pass_rate": pass_rate(group),
            "seed_mean": statistics.mean(seed_rates) if seed_rates else 0.0,
            "seed_stdev": (statistics.stdev(seed_rates)
                           if len(seed_rates) >= 2 else 0.0),
            "n_seeds": len(seed_rates),
        })
    return out


def per_model_condition_stratum(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    keys = ("model", "condition", "_stratum")
    for (model, cond, stratum), group in sorted(by_keys(rows, keys).items()):
        out.append({
            "model": model, "condition": cond, "stratum": stratum,
            "n_rows": len(group), "pass_rate": pass_rate(group),
            "n_problems": len({r["problem"] for r in group}),
        })
    return out


def failure_distribution(rows: list[dict]) -> list[dict]:
    failed = [r for r in rows if not r["passed"]]
    out: list[dict] = []
    for (model, stratum), group in sorted(
            by_keys(failed, ("model", "_stratum")).items()):
        cats: dict[str, int] = defaultdict(int)
        for r in group:
            cats[r.get("category", "other")] += 1
        out.append({
            "model": model, "stratum": stratum,
            "n_failures": len(group),
            **{f"cat_{k}": v for k, v in sorted(cats.items())},
        })
    return out


def md_table(rows: list[dict], cols: list[str]) -> str:
    if not rows:
        return "_(no rows)_\n"
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = []
    for r in rows:
        cells = []
        for c in cols:
            v = r.get(c, "")
            if isinstance(v, float):
                cells.append(f"{v:.3f}")
            else:
                cells.append(str(v))
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep, *body]) + "\n"


def render(rows: list[dict]) -> str:
    union, inter, n_problems = pool_pass_rates(rows)
    parts: list[str] = []
    parts.append("# Aggregation report\n")
    parts.append(f"- Input rows: **{len(rows)}**\n")
    parts.append(f"- Distinct problems covered: **{n_problems}**\n")
    parts.append(f"- Distinct (model, condition) cells: "
                 f"**{len({(r['model'], r['condition']) for r in rows})}**\n")

    parts.append("\n## 1. Pool pass-rate\n")
    parts.append(
        f"- **Union pass-rate** (problem solved by ≥1 model/seed/condition): "
        f"**{union:.3f}**\n"
    )
    parts.append(
        f"- **Intersection pass-rate** (problem solved by every model+seed in "
        f"some condition): **{inter:.3f}**\n"
    )

    parts.append("\n## 2. Per-(model, condition) overall\n")
    parts.append(md_table(per_model_condition(rows), [
        "model", "condition", "n_rows", "n_problems", "n_seeds",
        "pass_rate", "seed_mean", "seed_stdev",
    ]))

    parts.append("\n## 3. Per-(model, condition, stratum)\n")
    parts.append(md_table(per_model_condition_stratum(rows), [
        "model", "condition", "stratum", "n_problems", "n_rows", "pass_rate",
    ]))

    parts.append("\n## 4. Failure-category distribution\n")
    fd = failure_distribution(rows)
    label_cols = ["model", "stratum", "n_failures"]
    cat_cols = sorted({k for r in fd for k in r if k.startswith("cat_")})
    parts.append(md_table(fd, label_cols + cat_cols))

    return "\n".join(parts)


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("")
        return
    cols = sorted({k for r in rows for k in r})
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("inputs", nargs="+", type=Path,
                        help="Result JSONL files or directories.")
    parser.add_argument("--csv-dir", type=Path,
                        help="If set, also write per-table CSVs here.")
    args = parser.parse_args()

    paths: list[Path] = []
    for p in args.inputs:
        if p.is_dir():
            paths.extend(sorted(p.glob("*.jsonl")))
        else:
            paths.append(p)
    if not paths:
        print("ERROR: no input JSONL files found", file=sys.stderr)
        return 1

    rows = load_rows(paths)
    if not rows:
        print("ERROR: input files contained no rows", file=sys.stderr)
        return 1

    sys.stdout.write(render(rows))

    if args.csv_dir:
        args.csv_dir.mkdir(parents=True, exist_ok=True)
        write_csv(args.csv_dir / "per_model_condition.csv",
                  per_model_condition(rows))
        write_csv(args.csv_dir / "per_model_condition_stratum.csv",
                  per_model_condition_stratum(rows))
        write_csv(args.csv_dir / "failure_distribution.csv",
                  failure_distribution(rows))
        flat = [{k: v for k, v in r.items() if not k.startswith("_") or k == "_stratum"}
                for r in rows]
        for r in flat:
            r["stratum"] = r.pop("_stratum", "?")
        write_csv(args.csv_dir / "rows.csv", flat)
        print(f"\nWrote CSVs to {args.csv_dir}/", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())