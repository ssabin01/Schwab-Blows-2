# DB Schema — AegisRisk (conceptual)

Local-first persistence is recommended for MVP. SQLite is a practical default.

## Core tables
### instruments
- instrument_id (pk)
- symbol
- type (STOCK, OPTION)
- multiplier
- currency
- metadata_json

### option_contracts
- option_contract_id (pk)
- underlying_symbol
- expiry
- strike
- right (C/P)
- style (AMERICAN/EUROPEAN/UNKNOWN)
- settlement
- provider_contract_key

### trade_versions
- trade_version_id (pk)
- trade_hash (unique)
- name
- created_at
- trade_json (immutable full definition)

### trade_drafts
- trade_draft_id (pk)
- rev (monotonic int)
- name
- updated_at

### trade_draft_legs
- leg_id (pk)
- trade_draft_id (fk)
- instrument_ref (option_contract_id or symbol)
- signed_qty
- entry_price
- fees
- include_flag (bool)
- created_at
- updated_at

### market_snapshots
- snapshot_id (pk)
- snapshot_hash (unique)
- symbol
- mode (LIVE/PINNED)
- created_at
- source
- overrides_json (rates/div inputs)
- diagnostics_json

### snapshot_underlying_quotes
- snapshot_id (fk)
- spot
- bid
- ask
- last
- provider_timestamp
- receive_timestamp

### snapshot_option_quotes
- snapshot_id (fk)
- option_contract_id (fk)
- bid
- ask
- mark
- iv
- provider_timestamp
- receive_timestamp

### model_configs
- model_config_id (pk)
- model_config_hash (unique)
- config_json
- created_at

### scenario_grids
- scenario_grid_id (pk)
- scenario_grid_hash (unique)
- grid_json
- created_at

### analytics_results
- result_id (pk)
- trade_ref_type (DRAFT/VERSION)
- trade_ref_id
- snapshot_id
- model_config_id
- scenario_grid_id
- measures_json
- outputs_blob_or_json
- warnings_json
- errors_json
- created_at

### pnl_attribution_results
- attribution_id (pk)
- trade_ref_type
- trade_ref_id
- snapshot_id
- model_config_id
- base_state_json
- compare_state_json
- method
- outputs_json
- warnings_json
- errors_json
- created_at

### audit_log
- audit_id (pk)
- timestamp
- actor (local user)
- event_type
- event_payload_json

## Secrets
Do not store OAuth tokens in the DB unencrypted. Prefer OS keychain; otherwise, encrypt-at-rest with a key not stored alongside ciphertext.
