# Rates / Dividends / Borrow Policy (MVP)

This document locks **where r, q, and borrow come from** and how they are applied.

If any other document conflicts with this file, **this file wins**.

---

## Goal

We need deterministic, auditable IV/Greeks calculations.

Therefore:
- r / q / borrow must be **explicit inputs**
- they must be persisted
- they must be hashed into the run identifier

No implicit “magic” provider inference is allowed in MVP.

---

## Definitions

- **r** = risk-free rate (continuous compounding)
- **q** = continuous dividend yield
- **borrow** = stock borrow / financing spread (separate from q)

---

## Source of Truth (MVP)

### Primary Source: ModelConfig (manual inputs)
In MVP, the system MUST take r, q, borrow from `ModelConfig`.

Defaults:
- r = 0.00
- q = 0.00
- borrow = 0.00

Users may override these values explicitly.

### Prohibited in MVP
- Fetching a yield curve from any provider
- Inferring dividend yield from historical dividends
- Auto-detecting borrow from any external source

Rationale:
- provider data availability is uncertain
- inference is non-deterministic and creates silent drift
- we prioritize correctness and auditability over convenience

---

## Application Rules

- r, q, borrow are applied consistently for:
  - IV inversion
  - pricing
  - Greeks
  - scenario evaluation

- Any change to r/q/borrow invalidates cached outputs and creates a new run ID.

---

## Persistence and Audit

Each run MUST persist:
- the exact r/q/borrow used
- the full `ModelConfig` blob
- the MarketSnapshot ID(s)

Same snapshot + same model config MUST reproduce the same numbers.

---

## Future (Non-MVP)

A future phase may add optional provider-backed curves or dividend schedules, but only if:
- the provider source is explicitly recorded
- the fetched curve/schedule is snapshotted and stored
- parity tests cover the change

This is not part of MVP.
