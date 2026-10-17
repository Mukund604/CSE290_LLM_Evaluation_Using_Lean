#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

DATASET = Path("datasets/miniF2F_v2c.json")

SYSTEM_BASELINE = """You are a Lean 4 (with Mathlib) proof assistant.

You will be given a theorem statement ending in `:= by`. Produce ONLY the
body of the `by` block — the tactic block that would be substituted for
`sorry`.

Rules:
- Output a SINGLE fenced code block: ```lean ... ```
- Inside the fence, write ONLY the tactic block. No `theorem` line, no
  imports, no Markdown commentary. The text inside the fence will be
  appended verbatim after `:= by` and must compile under Lean 4 with
  `import Mathlib`.
- Use 2-space indentation; do not include leading or trailing blank lines.
- Already in scope: `import Mathlib`, `import Aesop`, and the namespaces
  BigOperators, Real, Nat, Rat, Finset, Topology.
- A bare one-liner closer (`decide`, `nlinarith`, `polyrith`, `omega`,
  `aesop`) is acceptable IF it actually closes the goal.
"""

SYSTEM_SKETCH = """You are a Lean 4 (with Mathlib) proof assistant.

You will be given a theorem statement ending in `:= by`. Work in TWO steps:

Step 1 — Informal sketch. In plain prose (NOT a code block), write a short
informal proof sketch: identify the key lemma or algebraic step, name the
tactic strategy you plan to use, and flag any side conditions. Aim for
3–8 sentences. Do not put this sketch inside a fenced code block.

Step 2 — Formal proof. Output a SINGLE fenced code block: ```lean ... ```
Inside the fence, write ONLY the tactic block (the body of the `by` block).

Rules for the fenced block (identical to the baseline condition):
- No `theorem` line, no imports, no Markdown commentary inside the fence.
  The text inside the fence will be appended verbatim after `:= by` and
  must compile under Lean 4 with `import Mathlib`.
- Use 2-space indentation; do not include leading or trailing blank lines.
- Already in scope: `import Mathlib`, `import Aesop`, and the namespaces
  BigOperators, Real, Nat, Rat, Finset, Topology.
- A bare one-liner closer (`decide`, `nlinarith`, `polyrith`, `omega`,
  `aesop`) is acceptable IF it actually closes the goal.
- Only the FIRST ```lean ... ``` block is parsed; do not write a second one.
"""

USER_TMPL_BASELINE = """Prove the following theorem.

```lean
{header}{formal_statement}
  sorry
```

Reply with just the ```lean ... ``` fenced block containing the tactic body.
"""

USER_TMPL_SKETCH = """Prove the following theorem.

```lean
{header}{formal_statement}
  sorry
```

First write the informal sketch (plain prose, no code fence), then the
single ```lean ... ``` fenced block containing the formal tactic body.
"""

CONDITION_PROMPTS = {
    "baseline": (SYSTEM_BASELINE, USER_TMPL_BASELINE),
    "informal_sketch": (SYSTEM_SKETCH, USER_TMPL_SKETCH),
}

FENCE_RE = re.compile(r"```(?:lean)?\s*\n(.*?)```", re.DOTALL)

def extract_proof(text: str) -> str:
    m = FENCE_RE.search(text)
    body = m.group(1) if m else text
    lines = body.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    indents = [len(l) - len(l.lstrip(" ")) for l in lines if l.strip()]
    dedent = min(indents) if indents else 0
    lines = [(l[dedent:] if l.strip() else "") for l in lines]
    if lines and lines[0].strip() == "by":
        lines = lines[1:]
    elif lines and lines[0].lstrip().startswith("by "):
        lines[0] = lines[0].replace("by ", "", 1)
    return "\n".join(lines)


def render_prompt(problem: dict, condition: str) -> tuple[str, str]:
    system, user_tmpl = CONDITION_PROMPTS[condition]
    user = user_tmpl.format(
        header=problem["header"],
        formal_statement=problem["formal_statement"],
    )
    return system, user


CALL_TIMEOUT_S = 300


def call_anthropic(model: str, problem: dict, temperature: float,
                   max_tokens: int, condition: str) -> str:
    import anthropic
    system, user = render_prompt(problem, condition)
    client = anthropic.Anthropic(timeout=CALL_TIMEOUT_S)
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(b.text for b in resp.content
                   if getattr(b, "type", None) == "text")


def call_openai(model: str, problem: dict, temperature: float,
                max_tokens: int, condition: str) -> str:
    from openai import OpenAI
    system, user = render_prompt(problem, condition)
    client = OpenAI(timeout=CALL_TIMEOUT_S)
    resp = client.responses.create(
        model=model,
        instructions=system,
        input=user,
        max_output_tokens=max_tokens,
    )
    return resp.output_text or ""


def call_openrouter(model: str, problem: dict, temperature: float,
                    max_tokens: int, condition: str) -> str:
    import os
    from openai import OpenAI
    system, user = render_prompt(problem, condition)
    client = OpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
        timeout=CALL_TIMEOUT_S,
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content or ""


def call_google(model: str, problem: dict, temperature: float,
                max_tokens: int, condition: str) -> str:
    from google import genai
    from google.genai import types
    system, user = render_prompt(problem, condition)
    client = genai.Client(http_options={"timeout": CALL_TIMEOUT_S * 1000})
    resp = client.models.generate_content(
        model=model,
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            temperature=temperature,
            max_output_tokens=max_tokens,
        ),
    )
    return resp.text or ""


CALLERS = {"anthropic": call_anthropic, "google": call_google,
           "openai": call_openai, "openrouter": call_openrouter}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--provider", choices=CALLERS.keys(), required=True)
    parser.add_argument("--model", required=True,
                        help="e.g. claude-opus-4-7, gemini-2.5-pro")
    parser.add_argument("--problem", action="append",
                        help="Problem name (repeatable). Defaults to the "
                             "30-problem evaluation subset from "
                             "build_problems.SUBSET. Use --all to opt in to "
                             "the full 244-problem test split.")
    parser.add_argument("--all", action="store_true",
                        help="Generate for all 244 test-split problems "
                             "instead of just the 30-problem subset. "
                             "USE WITH CAUTION: ~8x cost.")
    parser.add_argument("--seed", type=int, default=0,
                        help="Recorded in output rows. Note: most provider "
                             "APIs do not honor a seed parameter; rerun with "
                             "different --seed values to get different samples.")
    parser.add_argument("--condition", default="baseline",
                        choices=sorted(CONDITION_PROMPTS),
                        help="Prompt condition. baseline = formal proof only. "
                             "informal_sketch = informal sketch then formal proof.")
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--max-tokens", type=int, default=32768,
                        help="Output token budget (default: 32768). Reasoning "
                             "models consume part of this on internal thinking; "
                             "a budget below ~16384 silently truncates the "
                             "fenced Lean block to empty.")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    load_dotenv()

    dataset = {p["name"]: p for p in json.loads(DATASET.read_text())
               if p["split"] == "test"}
    if args.problem:
        names = args.problem
    elif args.all:
        names = sorted(dataset)
    else:
        from build_problems import SUBSET_NAMES
        names = SUBSET_NAMES
    missing = [n for n in names if n not in dataset]
    if missing:
        sys.exit(f"ERROR: unknown problems: {missing}")

    caller = CALLERS[args.provider]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as out:
        for name in names:
            start = time.monotonic()
            try:
                raw = caller(args.model, dataset[name],
                             args.temperature, args.max_tokens,
                             args.condition)
            except Exception as e:
                raw = ""
                err = f"{type(e).__name__}: {e}"
                print(f"  {name} ERROR {err}", file=sys.stderr)
            else:
                err = ""
            proof = extract_proof(raw)
            row = {
                "problem": name,
                "proof": proof,
                "model": args.model,
                "seed": args.seed,
                "condition": args.condition,
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
