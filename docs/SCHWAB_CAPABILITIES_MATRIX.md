# Schwab Capabilities Matrix (MVP)

This document defines how the app discovers and handles Schwab API capability differences
(entitlements, fields present, streaming availability).

If any other document conflicts with this file, **this file wins**.

---

## Goal

Build a deterministic, auditable risk engine that works even when Schwab capabilities vary.

Therefore:
- We MUST feature-detect Schwab capabilities at runtime (or via a one-time probe).
- We MUST NOT assume implied volatility or streaming exists.
- We MUST NOT block development waiting for entitlements.

---

## Capabilities We Care About

### C1. Underlying Quote Fields
Required:
- bid, ask, last (or equivalent)
Derived:
- mark = (bid + ask) / 2 when both present

### C2. Option Chain Retrieval
Required:
- contract identifiers (expiry, strike, right, symbol)
- bid, ask, last (or equivalent)
Derived:
- mark = (bid + ask) / 2 when both present

### C3. Per-Contract Implied Volatility
Optional but critical for `RAW_CHAIN_IV` mode.

- If present: we ingest it and store it in MarketSnapshot.
- If absent: MarketSnapshot must explicitly mark IV as missing.

### C4. Streaming (Tick-by-Tick)
Optional optimization.
- If present: allowed only as a transport; must still produce snapshots.
- If absent: polling remains the baseline.

---

## Mandatory MVP Behavior (No Entitlement Assumptions)

The system MUST implement:
1. Polling-based snapshot ingestion (see `SCHWAB_INGESTION_POLICY.md`)
2. Feature detection:
   - detect whether option-chain IV field exists (C3)
   - detect whether streaming is available (C4), if applicable
3. Explicit error surfacing:
   - if C3 is missing and `ModelConfig.vol_mode = RAW_CHAIN_IV` and missing-IV policy is FAIL,
     calculations must fail closed with a clear message:
     "Schwab chain IV not available under current entitlement."

No synthetic IV may be invented unless explicitly enabled by a fallback policy.

---

## Capability Probe (Required)

MVP must include a probe command (CLI or internal dev command) that records:

- which quote fields are present for an underlying
- which option chain fields are present per contract (including IV if present)
- whether any streaming endpoints are accessible (if implemented)
- raw response sample hashes (or stored raw response for audit)

Output must be written to a local file:
- `artifacts/schwab_capabilities.json`

This file is used for:
- debugging
- audit
- determining whether ToS-parity validation is feasible on the current account

---

## Determinism Requirements

Even when capabilities vary:
- snapshots must be immutable
- missing fields must be explicit
- the same raw response must normalize into the same MarketSnapshot

---

## Non-Goals (MVP)

- guaranteeing tick-by-tick data for all accounts
- building a full entitlement management UI
- supporting multiple brokers

---

## Summary

Codex must build assuming:
- polling works
- streaming may not
- chain IV may not

And must fail closed where ToS-parity inputs are unavailable.
