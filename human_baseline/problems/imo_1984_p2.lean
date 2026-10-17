-- Problem: imo_1984_p2
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: C. Contamination probe (edited from v1, v2c≠v2s)
-- Why this problem: Existence: (a,b) with 7∤ab(a+b) and 7^7 ∣ (a+b)^7−a^7−b^7.
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
--   Find one pair of positive integers $a,b$ such that $ab(a+b)$ is not
--   divisible by $7$, but $(a+b)^7-a^7-b^7$ is divisible by $7^7$.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem imo_1984_p2 :
  ∃ (a b : ℕ), 0 < a ∧ 0 < b ∧ (¬ 7 ∣ a * b * (a + b)) ∧ ((7^7) ∣ ((a + b)^7 - a^7 - b^7)) := by
  sorry
