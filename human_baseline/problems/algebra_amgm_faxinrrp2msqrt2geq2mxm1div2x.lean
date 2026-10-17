-- Problem: algebra_amgm_faxinrrp2msqrt2geq2mxm1div2x
-- Source: miniF2F-v2 (v2c, test split) — Ospanov et al. 2025
-- Stratum: D. Unchanged from v1 (memorization-friendly control)
-- Why this problem: Classic AMGM consequence; statement identical to v1.
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
--   Let $x$ be a positive real number. Show that $2 - \sqrt{2} \geq 2 - x -
--   \frac{1}{2x}$.

import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Rat Finset Topology

theorem algebra_amgm_faxinrrp2msqrt2geq2mxm1div2x :
  ∀ x > 0, 2 - Real.sqrt 2 ≥ 2 - x - 1 / (2 * x) := by
  sorry
