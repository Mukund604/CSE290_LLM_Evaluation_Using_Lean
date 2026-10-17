-- Problem: imo_1966_p5
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: H. Hard / specialist-prover failure proxy
-- Why this problem: Linear system over |a_i−a_j|; case analysis on order.
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
--   Solve the system of equations   $|a_1 - a_2| x_2 +|a_1 - a_3| x_3 +|a_1 -
--   a_4| x_4 = 1\\ |a_2 - a_1| x_1 +|a_2 - a_3| x_3 +|a_2 - a_4| x_4 = 1\\
--   |a_3 - a_1| x_1 +|a_3 - a_2| x_2 +|a_3-a_4|x_4= 1\\ |a_4 - a_1| x_1 +|a_4
--   - a_2| x_2 +|a_4 - a_3| x_3 = 1$   where $a_1, a_2, a_3, a_4$ are four
--   different real numbers.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

abbrev imo_1966_p5_solution : (ℝ×ℝ×ℝ×ℝ) → (ℝ×ℝ×ℝ×ℝ) := sorry

theorem imo_1966_p5_v2c
  (x a : ℕ → ℝ)
  (i j k l : ℕ)
  (s : Finset ℕ)
  (hs₀ : s = Finset.Icc 1 4)
  (h₀ : a 1 ≠ a 2)
  (h₁ : a 1 ≠ a 3)
  (h₂ : a 1 ≠ a 4)
  (h₃ : a 2 ≠ a 3)
  (h₄ : a 2 ≠ a 4)
  (h₅ : a 3 ≠ a 4)
  (h₆ : abs (a 1 - a 2) * x 2 + abs (a 1 - a 3) * x 3 + abs (a 1 - a 4) * x 4 = 1)
  (h₇ : abs (a 2 - a 1) * x 1 + abs (a 2 - a 3) * x 3 + abs (a 2 - a 4) * x 4 = 1)
  (h₈ : abs (a 3 - a 1) * x 1 + abs (a 3 - a 2) * x 2 + abs (a 3 - a 4) * x 4 = 1)
  (h₉ : abs (a 4 - a 1) * x 1 + abs (a 4 - a 2) * x 2 + abs (a 4 - a 3) * x 3 = 1) :
  (x 1, x 2, x 3, x 4) = imo_1966_p5_solution (a 1, a 2, a 3, a 4) := by
  sorry
