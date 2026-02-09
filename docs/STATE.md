# State — AegisRisk

## Current status

## Bootstrap complete
- Standard commands exist (`make setup`, `make lint`, `make test`) per `/docs/AGENTS.md`.
- Minimal Python analytics core exists:
  - Black–Scholes prices/greeks (goldens: BS-1, BS-2)
  - CRR binomial (American invariants: AM-1, AM-2)
- Deterministic hashing helpers added (fail-closed on NaN/Inf).

- Not implemented yet. This file becomes the handoff anchor after every work session.

## Next 3 tasks
1) Implement provider adapter interface + mock provider
2) Implement TradeDraft + MarketSnapshot + hashing
3) Implement chain browser + click-to-add legs

## Open decisions
- UI stack and charting approach
- American option pricing backend choice for MVP
- Rates/dividend input default policy for snapshots
