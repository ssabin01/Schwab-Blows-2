# Schwab Market Data Ingestion Policy (MVP)

This document defines how market data is ingested from the Schwab API.

If any other document conflicts with this file, **this file wins**.

---

## Scope

This policy applies to:
- underlying quotes
- option chain quotes
- implied volatility fields (if available)

Order routing, execution, and account state are explicitly out of scope.

---

## Ingestion Model

### Snapshot-Based Ingestion

All data from Schwab MUST be ingested into immutable **MarketSnapshots**.

- Schwab is never queried directly by pricing or UI code
- All calculations use snapshot data only
- Every snapshot is replayable

---

## Live Data Behavior

Live data MUST behave as real-time, but correctness takes priority over raw tick throughput.

Rules:
- Ingest updates as frequently as allowed by Schwab
- Coalesce updates to **latest snapshot only**
- Never queue or replay stale ticks
- Skip intermediate updates if required

This matches institutional risk systems and prevents backlog-induced latency.

---

## Transport

### Baseline (MVP)
- **HTTP polling**
- Poll interval governed by `SNAPSHOT_POLICY.md`
- All requests must be idempotent

### Streaming (Optional, Non-MVP)
- Streaming may be enabled only if:
  - Schwab entitlements permit it
  - Message semantics are well-defined
- Streaming MUST still produce snapshots
- Streaming MUST obey the same coalescing rules

Streaming is an optimization, not a requirement.

---

## Required Fields (Minimum)

A MarketSnapshot MUST include, if available:

### Underlying
- symbol
- bid
- ask
- mark
- last
- timestamp

### Options (per contract)
- symbol
- strike
- expiration
- right (call/put)
- bid
- ask
- mark
- last
- implied volatility (if provided by Schwab)

Absence of implied volatility MUST be explicit.

---

## Entitlement Reality

Schwab API capabilities vary by account and approval.

Therefore:
- Code MUST NOT assume implied volatility is present
- Code MUST NOT assume streaming is available
- Missing data MUST be surfaced explicitly
- No synthetic data may be invented

---

## Failure Behavior

If Schwab returns:
- partial data → snapshot is still created with missing fields flagged
- errors → last good snapshot remains active
- stale timestamps → snapshot is rejected

Errors must be visible to the user.

---

## Audit Requirements

For every snapshot:
- persist raw Schwab response (or canonical hash)
- persist normalized snapshot
- persist timestamp and request metadata

Same raw inputs MUST always produce the same snapshot.

---

## Explicit Non-Goals

- Reconstructing tick-by-tick history
- Microsecond latency guarantees
- Best-execution analysis
- Provider failover

This is a decision-support system, not an OMS.
