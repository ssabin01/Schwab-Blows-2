PROJECT_CAPSULE.md

# Project Capsule — AegisRisk

## What it is
AegisRisk is a compare-first options risk workbench: build or import two trades, evaluate them under a single shared scenario definition, and inspect A, B, and A–B differences with synchronized inspection (crosshair/cell selection) and diff-first tables.

## What it is not
- Not a broker / execution platform
- Not an order ticket / routing system
- Not an OMS/EMS

## MVP headline capabilities
1. Compare Workspace with Trade A + Trade B side-by-side.
2. Live options chain browser:
   - Click ask = add buy (long) leg
   - Click bid = add sell (short) leg
   - Hold Control (macOS) to accumulate multiple clicks into a multi-leg trade build session
3. Stacked charts per trade: Primary measure + Value + Greeks strip (Δ/Γ/Θ/ν).
4. Scenario grids:
   - Spot × Time (curves)
   - Spot × Vol (matrix)
5. Tables (table-first UI):
   - Price Slices table (includes “Live” row driven by inspection cursor/cell)
   - Positions/legs table with include/exclude checkboxes
   - PnL Attribution table (Taylor 2nd-order + residual)

## Determinism rule
All analytics results must be reproducible from:
- Trade version hash
- MarketSnapshot id/hash
- ScenarioGrid hash
- ModelConfig hash/version
Plus explicit floating tolerances.

## Primary integration (MVP)
Schwab adapter for read-only:
- account positions (optional for MVP)
- market data (required for MVP chain + snapshots)
Exact endpoints/scopes are entitlement-dependent and must be confirmed in provider documentation and approvals.

## Big risks to manage early
- Market data availability/entitlements (chains + IV + timestamp fidelity)
- UI performance for dense chains and fast inspection
- Auditability vs “live updating”: need snapshot pinning and replay