#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

from build_problems import SUBSET  # type: ignore

STRATUM_OF = {name: code for code, _, name, _ in SUBSET}
STRATA_ORDER = sorted({code for code, _, _, _ in SUBSET})

def load_rows(paths: list[Path]) -> list[dict]:
    out: list[dict] = []
    for p in paths:
        if p.is_dir():
            for q in sorted(p.glob("*.jsonl")):
                out.extend(load_rows([q]))
            continue
        for line in p.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            r.setdefault("condition", "baseline")
            r["_stratum"] = STRATUM_OF.get(r["problem"], "?")
            out.append(r)
    return out


def plot_passrate_by_model_stratum(rows: list[dict], out: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    by_model_stratum_seed: dict = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r.get("condition") != "baseline":
            continue
        by_model_stratum_seed[r["model"]][(r["_stratum"], r["seed"])].append(
            bool(r["passed"]))

    models = sorted(by_model_stratum_seed)
    if not models:
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    width = 0.8 / max(len(models), 1)
    x = np.arange(len(STRATA_ORDER))

    for i, m in enumerate(models):
        means, errs = [], []
        for s in STRATA_ORDER:
            seed_rates = []
            for (stratum, seed), bools in by_model_stratum_seed[m].items():
                if stratum == s and bools:
                    seed_rates.append(sum(bools) / len(bools))
            means.append(statistics.mean(seed_rates) if seed_rates else 0.0)
            errs.append(statistics.stdev(seed_rates)
                        if len(seed_rates) >= 2 else 0.0)
        ax.bar(x + i * width - 0.4 + width / 2, means, width,
               yerr=errs, capsize=3, label=m)

    ax.set_xticks(x)
    ax.set_xticklabels(STRATA_ORDER)
    ax.set_xlabel("Stratum")
    ax.set_ylabel("Pass rate (baseline, mean across seeds)")
    ax.set_title("Pass-rate by model and stratum (error bars: across-seed std)")
    ax.set_ylim(0, 1.05)
    ax.legend()
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def plot_passrate_by_model_condition(rows: list[dict], out: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    pairs: dict = defaultdict(list)
    for r in rows:
        pairs[(r["model"], r["condition"])].append(bool(r["passed"]))

    if not pairs:
        return

    models = sorted({m for m, _ in pairs})
    conditions = sorted({c for _, c in pairs})
    if len(conditions) < 2 and not any(c != "baseline" for _, c in pairs):
        pass

    fig, ax = plt.subplots(figsize=(7, 4.5))
    width = 0.8 / max(len(conditions), 1)
    x = np.arange(len(models))
    for i, c in enumerate(conditions):
        ys = [statistics.mean(pairs[(m, c)]) if pairs[(m, c)] else 0.0
              for m in models]
        ax.bar(x + i * width - 0.4 + width / 2, ys, width, label=c)
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_ylabel("Pass rate")
    ax.set_title("Pass-rate by model and condition")
    ax.set_ylim(0, 1.05)
    ax.legend()
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def plot_failure_categories(rows: list[dict], out: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    cat_field = "hand_category" if any(r.get("hand_category")
                                       for r in rows) else "category"
    failed = [r for r in rows if not r["passed"]]
    if not failed:
        return

    by_model: dict = defaultdict(lambda: defaultdict(int))
    for r in failed:
        by_model[r["model"]][r.get(cat_field, "other") or "other"] += 1

    models = sorted(by_model)
    cats = sorted({c for d in by_model.values() for c in d})

    fig, ax = plt.subplots(figsize=(8, 5))
    bottom = np.zeros(len(models))
    for c in cats:
        ys = np.array([by_model[m].get(c, 0) for m in models])
        ax.bar(models, ys, bottom=bottom, label=c)
        bottom += ys
    ax.set_ylabel(f"Failures ({cat_field})")
    ax.set_title(f"Failure-category distribution per model ({cat_field})")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("inputs", nargs="+", type=Path,
                        help="Result JSONL files or directories.")
    parser.add_argument("--out-dir", type=Path, default=Path("harness/plots"),
                        help="Where to write PNGs (default: harness/plots).")
    args = parser.parse_args()

    rows = load_rows(args.inputs)
    if not rows:
        print("ERROR: no rows in input", file=sys.stderr)
        return 1

    args.out_dir.mkdir(parents=True, exist_ok=True)
    plot_passrate_by_model_stratum(rows, args.out_dir / "passrate_by_model_stratum.png")
    plot_passrate_by_model_condition(rows, args.out_dir / "passrate_by_model_condition.png")
    plot_failure_categories(rows, args.out_dir / "failure_categories.png")
    print(f"Wrote 3 PNGs to {args.out_dir}/", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
