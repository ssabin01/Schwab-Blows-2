# Contributing — AegisRisk

## Ground rules
- No guessing on market conventions: document decisions in an ADR.
- Every new analytic feature requires:
  - at least one validation case
  - metadata coverage (snapshot/config/grid hashes)
- No silent failure: warnings/errors must be explicit.

## Branching
- feature branches → PR → main
- PR must include:
  - tests
  - doc update (`/docs/STATE.md` at minimum)

## Code style
- Format-on-save recommended.
- Keep provider adapters behind interfaces.
- Keep analytics pure and deterministic (no implicit “latest market”).

## Tests
- Unit: math/pricing/greeks
- Integration: evaluation pipeline, snapshot building
- UI acceptance: crosshair/cell sync, chain-click behavior, table rendering
