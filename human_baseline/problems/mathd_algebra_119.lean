-- Problem: mathd_algebra_119
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: D. Unchanged from v1 (memorization-friendly control)
-- Why this problem: Two-equation linear system over integers; identical to v1.
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
--   Solve for $e$, given that $2d$ is $8$ less than $17e$, and $2e$ is $9$
--   less than $d$. Show that it is 2.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem mathd_algebra_119 (d e : ℝ) (h₀ : 2 * d = 17 * e - 8) (h₁ : 2 * e = d - 9) : e = 2 := by
  sorry
