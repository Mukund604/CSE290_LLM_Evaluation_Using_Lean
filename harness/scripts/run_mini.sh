#!/usr/bin/env bash
# 3-problem sentinel batch — runs BEFORE the full coverage-gap run.
# Same providers and prompt as run_gap.sh, but only 3 problems × 3 models × 1 seed = 9 calls.
# Expected total spend: ~$0.20 (Claude dominates).
#
# Picked problems span 3 of the 4 missing strata so the result is informative,
# not just a connectivity test:
#   - mathd_algebra_22         (A: easy algebra, expected pass — `norm_num [Real.logb]` territory)
#   - mathd_numbertheory_81    (E: number-theory tactic stress, expected pass — `decide`)
#   - induction_sum2kp1npqsqm1 (G: induction, expected mixed — exercises failure classifier)
#
# Usage: bash harness/scripts/run_mini.sh
# Outputs: attempts/mini_<model>_seed0.jsonl
#          harness/results/mini_<model>_seed0.jsonl (after verify)

set -euo pipefail
cd "$(dirname "$0")/../.."

PROBLEMS=(mathd_algebra_22 mathd_numbertheory_81 induction_sum2kp1npqsqm1)

# Confirm all 3 are missing for every model — fail loudly if any was already covered
.venv/bin/python - <<PY
import json, sys
from pathlib import Path
sys.path.insert(0, 'harness/scripts')
from build_problems import SUBSET_NAMES
mini = $(printf '"%s",' "${PROBLEMS[@]}" | sed 's/,$//' | awk '{printf "[%s]", $0}')
for tag in ("claude","gpt54","gemini"):
    seen = set()
    for s in (0,1,2):
        p = Path(f"harness/results/baseline_final_{tag}_seed{s}.jsonl")
        if p.exists():
            for line in p.read_text().splitlines():
                if line.strip():
                    seen.add(json.loads(line)["problem"])
    overlap = [m for m in mini if m in seen]
    if overlap:
        print(f"WARN {tag} already has data for: {overlap}", file=sys.stderr)
for m in mini:
    if m not in SUBSET_NAMES:
        sys.exit(f"FATAL: {m} not in 30-problem subset")
print("Mini-batch sentinel problems validated.", file=sys.stderr)
PY

run_one() {
  local tag="$1" provider="$2" model="$3"
  local out="attempts/mini_${tag}_seed0.jsonl"
  if [[ -s "$out" ]]; then
    echo "  $out already exists — skipping" >&2
    return 0
  fi
  local ARGS=()
  for p in "${PROBLEMS[@]}"; do ARGS+=(--problem "$p"); done
  echo "=== ${tag} mini: ${#PROBLEMS[@]} problems via ${provider}/${model} ===" >&2
  .venv/bin/python harness/scripts/generate.py \
    --provider "$provider" --model "$model" \
    "${ARGS[@]}" --seed 0 --condition baseline \
    --max-tokens 32768 \
    --output "$out" 2>&1 | tee "/tmp/_mini_${tag}.log" >&2 || true

  .venv/bin/python - <<PY
import json, sys
from pathlib import Path
rows = [json.loads(l) for l in Path("$out").read_text().splitlines() if l.strip()]
n = len(rows)
errs = [r for r in rows if r.get("error")]
empty = [r for r in rows if not r.get("error") and not r["proof"].strip()]
ok = n - len(errs) - len(empty)
elapsed = sum(r["elapsed_s"] for r in rows) / max(n,1)
print(f"  AUDIT: total={n} ok={ok} empty={len(empty)} errors={len(errs)} avg_elapsed={elapsed:.2f}s", file=sys.stderr)
hard = [r["error"] for r in errs if "402" in r.get("error","") or "Insufficient credits" in r.get("error","")]
if hard:
    print(f"  HARD STOP: {len(hard)} insufficient-credit errors", file=sys.stderr); sys.exit(99)
if errs and len(errs) == n:
    print(f"  HARD STOP: all calls errored", file=sys.stderr); sys.exit(99)
if empty and len(empty) == n:
    print(f"  HARD STOP: all calls returned empty output", file=sys.stderr); sys.exit(99)
PY
}

run_one claude openrouter anthropic/claude-opus-4.7
run_one gpt54  openai     gpt-5.4
run_one gemini openrouter google/gemini-2.5-pro

echo "=== Mini-batch generation complete. Verifying with Lean (600s timeout per problem)... ===" >&2

# Concatenate and verify
cat attempts/mini_*_seed0.jsonl > /tmp/_mini_all.jsonl
.venv/bin/python harness/scripts/run.py \
  --input /tmp/_mini_all.jsonl \
  --output harness/results/mini_combined_seed0.jsonl \
  --jobs 3 --timeout 600 2>&1 | tail -20

echo "=== Mini-batch result summary ===" >&2
.venv/bin/python - <<'PY'
import json
from pathlib import Path
rows = [json.loads(l) for l in Path("harness/results/mini_combined_seed0.jsonl").read_text().splitlines() if l.strip()]
by_model = {}
for r in rows:
    by_model.setdefault(r["model"], []).append(r)
for m, rs in by_model.items():
    n = len(rs); p = sum(1 for r in rs if r["passed"])
    cats = ",".join(f"{c}={sum(1 for r in rs if r['category']==c)}" for c in sorted({r["category"] for r in rs}))
    print(f"  {m}: {p}/{n} pass; categories: {cats}")
PY

echo "=== run_mini.sh done. Review above before launching the full gap. ===" >&2
