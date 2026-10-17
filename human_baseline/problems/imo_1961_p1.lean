-- Problem: imo_1961_p1
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: H. Hard / specialist-prover failure proxy
-- Why this problem: x+y+z=a, x²+y²+z²=b², xy=z² — multi-equation elimination.
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
--   Solve the system of equations:   <center> $ \begin{matrix} \quad x + y +
--   z \!\!\! &= a \; \, \\ x^2 +y^2+z^2 \!\!\! &=b^2 \\ \qquad \qquad xy
--   \!\!\!  &= z^2 \end{matrix} $ </center>   where $a $ and $b $ are
--   constants.  Give the conditions that $a $ and $b $ must satisfy so that
--   $x, y, z $ (the solutions of the system) are distinct positive numbers.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

abbrev imo_1961_p1_solution : ℝ → ℝ → Prop := sorry

theorem imo_1961_p1 (x y z a b : ℝ) (h₀ : 0 < x ∧ 0 < y ∧ 0 < z) (h₁ : x ≠ y) (h₂ : y ≠ z)
  (h₃ : z ≠ x) (h₄ : x + y + z = a) (h₅ : x ^ 2 + y ^ 2 + z ^ 2 = b ^ 2) (h₆ : x * y = z ^ 2) :
  imo_1961_p1_solution a b := by
  sorry
