# MVP Scope — AegisRisk

## In scope
### Market data
- Load underlying quote + option chain quotes for a selected symbol.
- Create MarketSnapshots from live data (auto-refresh allowed) with an option to pin/freeze a snapshot for reproducibility.

### Trade construction
- Trade A and Trade B editable drafts.
- Chain-driven leg creation:
  - ask click → add buy leg
  - bid click → add sell leg
  - Control key on macOS → multi-leg add session
- Manual editing:
  - qty, side, entry price, fees
  - add/remove legs (stock + options)
  - include/exclude legs via table checkboxes

### Analytics
- Measures: Value, P/L Open, Δ/Γ/Θ/ν
- Scenario grids:
  - Spot × Time (curves)
  - Spot × Vol (matrix)
- Caching so cursor movement and measure toggles don’t trigger full recompute.

### UI
- Compare Workspace: two columns A and B, stacked charts, synchronized inspection.
- Tables: Price Slices, Positions/legs, PnL Attribution.

## Out of scope
- Any order placement, ticketing, routing, execution
- Broker-dependent advanced features not required for read-only analysis
- Multi-account reporting

## Open items that must be decided early (but can be simple for MVP)
- Pricing backend choice for American options
- Rates/dividend input policy for snapshots (manual, provider, curve)
- Snapshot refresh cadence and what qualifies as “pinned”