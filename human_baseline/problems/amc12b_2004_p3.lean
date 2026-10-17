-- Problem: amc12b_2004_p3
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: C. Contamination probe (edited from v1, v2c≠v2s)
-- Why this problem: 2^x · 3^y = 1296; multiple-choice form retained.
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
--   If $x$ and $y$ are positive integers for which $2^x3^y=1296$, what is the
--   value of $x+y$? Prove that it is one of the following options.
--   $(\mathrm {A})\ 8 \qquad (\mathrm {B})\ 9 \qquad (\mathrm {C})\ 10 \qquad
--   (\mathrm {D})\ 11 \qquad (\mathrm {E})\ 12$

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem amc12b_2004_p3 (x y : ℕ) (hp: 0 < x ∧ 0 < y)
  (h₀ : 2 ^ x * 3 ^ y = 1296) :
  x + y = 8 ∨ x + y = 9 ∨ x + y = 10 ∨ x + y = 11 ∨ x + y = 12 := by
  sorry
