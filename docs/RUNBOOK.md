# Runbook — AegisRisk

## If option chain is empty / missing fields
1. Check provider entitlements and approval status.
2. Inspect adapter logs for the provider response shape (redacted).
3. Confirm symbol resolution and expiry filter.
4. If IV missing:
   - confirm RAW_CHAIN_IV policy and fallback behavior
   - verify warnings surfaced in UI

## If analytics values look wrong
1. Pin snapshot and rerun: confirm reproducibility.
2. Verify ModelConfig:
   - rates/div inputs
   - theta units
   - pricing backend id
3. Validate against golden cases in `/docs/VALIDATION_CASES.md` (BS-1/BS-2).
4. Check contract multiplier and signed quantity.

## If UI feels slow
1. Confirm caching is active (cache hit rate).
2. Ensure cursor movement uses cached arrays/matrices, not recompute.
3. Profile:
   - chain rendering
   - chart rendering
   - scenario evaluation

## If NaNs appear
- Treat as a defect: engine must return explicit error states, not NaNs.
- Add a regression test.
