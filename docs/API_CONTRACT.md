# Internal API Contract — AegisRisk (v0)

This is the UI ↔ local services contract. It is not a public API.

## Conventions
- All IDs are opaque strings.
- All responses include `warnings: []` and `errors: []` arrays.
- Version every breaking change.

## 1. Market data

### GET /v0/symbols/search?q=...
Returns matching underlyings.
Response:
- items: [{ symbol, description, asset_type }]

### GET /v0/market/underlying/{symbol}/quote
Response:
- { symbol, spot, bid?, ask?, last?, timestamp, source }

### GET /v0/market/options/{symbol}/chain?expiry=YYYY-MM-DD&range=...
Response:
- { symbol, expiries: [...], chain: [ { expiry, strike, right, bid, ask, mark?, iv?, volume?, oi?, timestamp } ] }

### POST /v0/snapshots
Create a snapshot from latest cached market data (or from provided overrides).
Request:
- { symbol, mode: "LIVE"|"PINNED", include_chain: true, overrides?: { r?, q? } }
Response:
- { snapshot_id, hash, timestamp, mode, diagnostics }

### POST /v0/snapshots/{snapshot_id}/pin
Response:
- { snapshot_id, mode:"PINNED" }

## 2. Trades

### POST /v0/trades/drafts
Request:
- { name?, base_on_trade_version_id? }
Response:
- { trade_draft_id, rev }

### GET /v0/trades/drafts/{trade_draft_id}
Response:
- { trade_draft_id, rev, legs:[...], fees_config? }

### POST /v0/trades/drafts/{trade_draft_id}/legs
Create leg (used by chain click).
Request:
- { instrument_type:"OPTION"|"STOCK", side:"LONG"|"SHORT", qty, entry_price, contract?:{symbol, expiry, strike, right}, stock?:{symbol} }
Response:
- { trade_draft_id, rev, leg_id }

### PATCH /v0/trades/drafts/{trade_draft_id}/legs/{leg_id}
Edit leg fields (qty, entry_price, include flag, etc.)

### DELETE /v0/trades/drafts/{trade_draft_id}/legs/{leg_id}

### POST /v0/trades/drafts/{trade_draft_id}/commit
Response:
- { trade_version_id, trade_hash }

## 3. Scenario + evaluation

### POST /v0/scenario-grids
Request:
- { grid_type:"SPOT_TIME_CURVES"|"SPOT_VOL_MATRIX", spot_axis:{...}, time_axis?:{...}, vol_axis?:{...} }
Response:
- { scenario_grid_id, hash }

### POST /v0/model-configs
Request:
- { pricing_backend_id, vol_mode:"RAW_CHAIN_IV"|"FITTED_SURFACE", conventions:{ day_count, theta_units }, policies:{ ... } }
Response:
- { model_config_id, hash }

### POST /v0/evaluate
Request:
- { trade_ref:{type:"DRAFT"|"VERSION", id}, snapshot_id, scenario_grid_id, model_config_id, measures:["VALUE","PNL_OPEN","DELTA","GAMMA","THETA","VEGA"] }
Response:
- { result_id, metadata:{...}, outputs:{ curves?:..., matrix?:..., tables?:... }, warnings, errors }

## 4. Attribution

### POST /v0/attribution
Request:
- { trade_ref, snapshot_id, model_config_id, base_state:{...}, compare_state:{...}, method:"TAYLOR_2ND_ORDER" }
Response:
- { attribution_id, table:{ trade_level:..., leg_level:... }, residual, warnings, errors }
