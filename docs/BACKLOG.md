# Backlog — AegisRisk (priority order)

## P0 — Foundation
1. Repo skeleton + docs integrated
   - Add all `/docs/*`
   - Add `/docs/STATE.md` workflow

2. Core domain models
   - TradeDraft, Leg, TradeVersion
   - MarketSnapshot + hashing
   - ScenarioGrid + hashing
   - ModelConfig + hashing

3. Provider adapter interface + mock provider
   - Symbol search
   - Underlying quote
   - Option chain retrieval

## P1 — MVP user-visible loop
4. Chain browser UI (read-only)
   - expiry selection, strike filters
   - bid/ask columns required

5. Chain click → trade builder (MVP critical)
   Acceptance criteria:
   - ask click creates long option leg with entry=ask
   - bid click creates short option leg with entry=bid
   - active trade target (A or B) is honored
   - Control key multi-add mode accumulates legs and recomputes once at end (debounced)
   - zero interaction routes orders

6. TradeDraft editing UI
   - Positions/legs table with include/exclude
   - edit qty, entry, delete
   - explicit dirty/recompute indicator

7. Scenario engine (curves)
   - spot axis generation
   - horizons generation with T+0 rule
   - cached evaluation outputs

8. Charts + synchronized crosshair (curves)
   - primary + value + greeks strip
   - crosshair readable on dark background
   - A and B sync

9. Price Slices table
   - Live row driven by crosshair
   - add/remove slices
   - shows A, B, A–B

10. P/L attribution (Taylor 2nd-order + residual)
   - trade-level + leg-level
   - reconciliation tests

## P2 — MVP matrix mode
11. Spot × Vol matrix evaluation
12. Matrix rendering + synchronized cell selection
13. A–B diff matrix (optional but recommended)

## P3 — Hardening
14. Fitted surface + arbitrage checks + diagnostics
15. Snapshot replay UI and export
16. Performance profiling and optimization pass
