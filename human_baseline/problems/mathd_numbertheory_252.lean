-- Problem: mathd_numbertheory_252
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: E. Number theory tactic stress
-- Why this problem: 7! mod 23 — factorial + modular reduction.
--
-- Author: (your name here)
--
-- Rules (see ../README.md):
--   * Tactic mode only.
--   * No bare one-liner closer as the entire proof (decide / nlinarith /
--     polyrith / omega / aesop alone is not a valid submission unless this
--     header explicitly says otherwise).
--   * Do NOT modify the `theorem ... := by` line below — it is the v2c
--     statement verbatim. Only replace the `sorry` with your proof.
--
-- Informal statement:
--   What is the remainder when $7!$ is divided by $23$?   (Note: $n!$ means
--   "n factorial", defined as the product of all integers from $1$ to $n$.)
--   Show that it is 3.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem mathd_numbertheory_252 : 7! % 23 = 3 := by
  sorry
