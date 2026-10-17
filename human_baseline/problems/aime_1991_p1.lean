-- Problem: aime_1991_p1
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: B. Mid-difficulty competition
-- Why this problem: Symmetric integer system.
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
--   Find $x^2+y^2_{}$ if $x_{}^{}$ and $y_{}^{}$ are positive integers such
--   that $\begin{align*} xy+x+y&=71, \\ x^2y+xy^2&=880. \end{align*}$ Show
--   that it is 146.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem aime_1991_p1 (x y : ℕ) (h₀ : 0 < x ∧ 0 < y) (h₁ : x * y + (x + y) = 71)
  (h₂ : x ^ 2 * y + x * y ^ 2 = 880) : x ^ 2 + y ^ 2 = 146 := by
  sorry
