-- Problem: aime_1996_p5
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: B. Mid-difficulty competition
-- Why this problem: Roots-of-cubic via elementary symmetric polynomials.
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
--   Suppose that the [[root]]s of $x^3+3x^2+4x-11=0$ are $a$, $b$, and $c$,
--   and that the roots of $x^3+rx^2+sx+t=0$ are $a+b$, $b+c$, and $c+a$. Find
--   $t$. Show that it is 23.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem aime_1996_p5 (a b c r s t : ℝ) (f g : ℝ → ℝ)
  (h₀ : ∀ x, f x = x ^ 3 + 3 * x ^ 2 + 4 * x - 11) (h₁ : ∀ x, g x = x ^ 3 + r * x ^ 2 + s * x + t)
  (h₂ : f a = 0) (h₃ : f b = 0) (h₄ : f c = 0) (h₅ : g (a + b) = 0) (h₆ : g (b + c) = 0)
  (h₇ : g (c + a) = 0) (h₈ : List.Pairwise (· ≠ ·) [a, b, c]) : t = 23 := by
  sorry
