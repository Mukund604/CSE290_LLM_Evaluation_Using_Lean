#!/usr/bin/env bash
# Safe launcher for the coverage-gap generation runs.
# - Reads missing-problem lists per model from attempts/_missing_*.txt
# - Runs (model, seed) batches sequentially
# - Aborts immediately on a 402 (insufficient credits) or all-empty batch
# - Logs progress to stderr; one JSONL per (model, seed) in attempts/
#
# Usage:
#   bash harness/scripts/run_gap.sh claude        # just Claude (all 3 seeds)
#   bash harness/scripts/run_gap.sh gpt54         # just GPT-5.4
#   bash harness/scripts/run_gap.sh gemini        # just Gemini
#   bash harness/scripts/run_gap.sh all           # all three (default)
#   bash harness/scripts/run_gap.sh all 0         # all three, only seed 0 (health check)

set -euo pipefail

cd "$(dirname "$0")/../.."

WHICH="${1:-all}"
ONLY_SEED="${2:-}"

run_batch() {
  local tag="$1"
  local provider="$2"
  local model="$3"
  local seed="$4"
  local missing_file="attempts/_missing_${tag}.txt"
  local out="attempts/gap_${tag}_seed${seed}.jsonl"

  if [[ ! -f "$missing_file" ]]; then
    echo "MISSING LIST NOT FOUND: $missing_file" >&2
    exit 2
  fi
  if [[ -s "$out" ]]; then
    echo "  $out already exists ($(wc -l <"$out") rows) — skipping" >&2
    return 0
  fi

  local ARGS=()
  while IFS= read -r p || [[ -n "$p" ]]; do
    [[ -n "$p" ]] && ARGS+=(--problem "$p")
  done < "$missing_file"
  local n=$(( ${#ARGS[@]} / 2 ))

  # Sanity guard: refuse to launch if the parsed count doesn't match the file's
  # non-blank line count. Catches missing-trailing-newline or parse drift.
  local expected=$(grep -c . "$missing_file")
  if [[ $n -ne $expected ]]; then
    echo "FATAL: parsed ${n} problems but file has ${expected} non-blank lines. Aborting batch." >&2
    exit 3
  fi

  echo "=== ${tag} seed ${seed}: ${n} problems via ${provider}/${model} ===" >&2
  .venv/bin/python harness/scripts/generate.py \
    --provider "$provider" --model "$model" \
    "${ARGS[@]}" --seed "$seed" --condition baseline \
    --max-tokens 32768 \
    --output "$out" 2>&1 | tee "/tmp/_gap_${tag}_seed${seed}.log" >&2 || true

  # Audit the batch
  .venv/bin/python - <<PY
import json, sys
from pathlib import Path
rows = [json.loads(l) for l in Path("$out").read_text().splitlines() if l.strip()]
n = len(rows)
errs = [r for r in rows if r.get("error")]
empty = [r for r in rows if not r.get("error") and not r["proof"].strip()]
ok = n - len(errs) - len(empty)
elapsed = sum(r["elapsed_s"] for r in rows) / max(n,1)
print(f"  BATCH AUDIT: total={n} ok={ok} empty={len(empty)} errors={len(errs)} avg_elapsed={elapsed:.2f}s", file=sys.stderr)
hard = [r["error"] for r in errs if "402" in r.get("error","") or "Insufficient credits" in r.get("error","")]
if hard:
    print(f"  HARD STOP: {len(hard)} insufficient-credit errors", file=sys.stderr)
    sys.exit(99)
if errs and len(errs) == n:
    print(f"  HARD STOP: all {n} calls errored", file=sys.stderr)
    sys.exit(99)
if empty and len(empty) == n:
    print(f"  HARD STOP: all {n} calls returned empty output", file=sys.stderr)
    sys.exit(99)
PY
}

run_model() {
  local tag="$1" provider="$2" model="$3"
  if [[ -n "$ONLY_SEED" ]]; then
    run_batch "$tag" "$provider" "$model" "$ONLY_SEED"
  else
    for s in 0 1 2; do
      run_batch "$tag" "$provider" "$model" "$s"
    done
  fi
}

case "$WHICH" in
  claude) run_model claude openrouter anthropic/claude-opus-4.7 ;;
  gpt54)  run_model gpt54  openai     gpt-5.4 ;;
  gemini) run_model gemini openrouter google/gemini-2.5-pro ;;
  all)
    run_model claude openrouter anthropic/claude-opus-4.7
    run_model gpt54  openai     gpt-5.4
    run_model gemini openrouter google/gemini-2.5-pro
    ;;
  *) echo "Unknown target: $WHICH (use: claude|gpt54|gemini|all)" >&2; exit 2 ;;
esac

echo "=== run_gap.sh done ===" >&2
