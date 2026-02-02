# Data Sources — AegisRisk

## 1. Primary provider (MVP): Schwab (read-only)
Use a provider adapter with explicit entitlements checks.

Required capabilities for MVP:
- Underlying quote retrieval (spot/bid/ask/last per provider)
- Option chain retrieval:
  - bid/ask required
  - IV strongly preferred (required if RAW_CHAIN_IV is used with no fallback)
- Account positions import (optional but recommended)

Provider details are entitlement- and approval-dependent. Do not hardcode assumptions; keep adapter behind an interface.

## 2. Rates / dividends
MVP can start with explicit user inputs recorded into MarketSnapshot and ModelConfig:
- flat risk-free rate
- flat dividend/borrow yield

Later:
- curve-based rates
- dividend forecasts / borrow feeds

## 3. Timestamp discipline
- Snapshot must record:
  - provider timestamps (if provided)
  - local receive timestamps
  - whether snapshot is live or pinned
- Analytics must reference snapshot id/hash, not “latest”.

## 4. Data licensing
Do not store or redistribute provider data beyond what the license allows. Treat this as a gate for persistence features.
