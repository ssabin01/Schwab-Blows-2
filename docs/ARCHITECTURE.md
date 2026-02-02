# Architecture — AegisRisk

## 1. High-level components
- UI Client (keyboard-forward terminal-style UI)
- Internal API (local service boundary)
- Market Data Service
  - provider adapter(s) (Schwab read-only primary)
  - normalization + caching
  - snapshot builder
- Analytics Service
  - scenario engine (curves + matrix)
  - pricing/greeks engine (fast backend + optional higher-precision backend)
  - attribution engine
  - vol surface service (raw IV baseline; fitted later)
- Snapshot Store (local-first persistence)
- Secrets storage (encrypted; OS keychain preferred on macOS)

## 2. Data flow (live session)
1. UI requests chain for a symbol/expiry.
2. Market Data Service fetches chain + underlying quote → produces Live MarketSnapshot.
3. UI click on bid/ask cell → creates leg in active TradeDraft with inferred side + entry.
4. Analytics Service evaluates TradeDraft + MarketSnapshot + ScenarioGrid + ModelConfig.
5. Results cached under stable keys; UI renders charts/tables and sync inspection state.

## 3. Determinism & auditability
Every AnalyticsResult stores:
- trade hash (draft version id or committed version hash)
- snapshot id/hash + timestamps + provenance
- model config hash/version
- scenario grid hash
- warnings/errors list (never silent NaNs)

## 4. Caching strategy
Cache key must include:
- trade_draft_id + draft_rev (or trade_version_hash)
- market_snapshot_id
- scenario_grid_hash
- model_config_hash

Cache must allow:
- measure toggle without recompute
- fast inspection readouts (crosshair/cell selection)
- leg include/exclude updates as incremental recompute where possible

## 5. UI synchronization strategy
- One global scenario state store.
- One inspection state store:
  - curves mode: spot + horizon index (or interpolated horizon)
  - matrix mode: spot index + vol shock index
- All panels subscribe to those two stores; no panel-owned scenario state in MVP.

## 6. Provider adapter boundary
Market data adapter interface must support:
- symbol search/resolve
- underlying quote
- option chain retrieval (bid/ask/mark/IV if available)
- timestamps and market session metadata if provided

Endpoints are provider-specific and entitlement-dependent; keep the adapter behind an interface.

## 7. Packaging (MVP)
Local-first is recommended:
- UI and API run on the same machine
- snapshot store is local (SQLite suggested, but not mandated)
- secrets stored via OS facilities
