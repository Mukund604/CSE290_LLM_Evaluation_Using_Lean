-- Problem: amc12a_2009_p5
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: C. Contamination probe (edited from v1, v2c≠v2s)
-- Why this problem: Cube with perturbed dimensions; original answer-choice framing.
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
--   One dimension of a cube is increased by $1$, another is decreased by $1$,
--   and the third is left unchanged. The volume of the new rectangular solid
--   is $5$ less than that of the cube. What was the volume of the cube? Prove
--   that it is one of the following options.   $\textbf{(A)}\ 8 \qquad
--   \textbf{(B)}\ 27 \qquad \textbf{(C)}\ 64 \qquad \textbf{(D)}\ 125 \qquad
--   \textbf{(E)}\ 216$

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem amc12a_2009_p5 (x : ℝ) (h₀ : x ^ 3 - (x + 1) * (x - 1) * x = 5) :
  x ^ 3 = 8 ∨ x ^ 3 = 27 ∨ x ^ 3 = 64 ∨ x ^ 3 = 125 ∨ x ^ 3 = 216 := by
  sorry
