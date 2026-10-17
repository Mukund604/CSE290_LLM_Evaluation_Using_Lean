#!/usr/bin/env python3
from __future__ import annotations
import re
from dataclasses import dataclass

PATTERNS: list[tuple[str, re.Pattern]] = [
    ("timeout", re.compile(r"^__HARNESS_TIMEOUT__$", re.MULTILINE)),
    ("sorry_present", re.compile(r"declaration uses [`'\"]sorry[`'\"]", re.IGNORECASE)),
    ("hallucinated_lemma", re.compile(
        r"unknown (?:identifier|constant|tactic)|"
        r"unknown free variable|"
        r"failed to synthesize", re.IGNORECASE)),
    ("type_mismatch", re.compile(
        r"type mismatch|"
        r"has type[^\n]*\n[^\n]*but is expected", re.IGNORECASE)),
    ("heavy_tactic_failed", re.compile(
        r"\b(nlinarith|polyrith|linarith|omega|decide|positivity|norm_num)\b"
        r"[^\n]*(?:failed|could not|did not|unsolved)", re.IGNORECASE)),
    ("tactic_failed", re.compile(
        r"[Tt]actic\s+[`'\"]?\w+[`'\"]?\s+failed", re.IGNORECASE)),
    ("unfocused_goals", re.compile(
        r"unsolved goals|"
        r"no goals to be solved|"
        r"unexpected.*goal", re.IGNORECASE)),
    ("syntax_error", re.compile(
        r"unexpected token|"
        r"expected '|"
        r"unterminated", re.IGNORECASE)),
]

@dataclass
class Classification:
    category: str
    matched_excerpt: str


def classify(stderr: str) -> Classification:
    if not stderr.strip():
        return Classification("other", "")
    for name, pat in PATTERNS:
        m = pat.search(stderr)
        if m:
            start = max(0, m.start() - 40)
            end = min(len(stderr), m.end() + 80)
            return Classification(name, stderr[start:end].replace("\n", " "))
    return Classification("other", stderr[:160].replace("\n", " "))


def is_pass(stderr: str, returncode: int) -> bool:
    if returncode != 0:
        return False
    if re.search(r"declaration uses [`'\"]sorry[`'\"]", stderr):
        return False
    if re.search(r"\berror:", stderr):
        return False
    return True


if __name__ == "__main__":
    import sys
    text = sys.stdin.read()
    cls = classify(text)
    print(f"{cls.category}\t{cls.matched_excerpt[:120]}")
