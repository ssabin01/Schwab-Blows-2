# Market Snapshot Policy (MVP)

This document locks the behavior of **Live** vs **Pinned** market snapshots.

If any other document conflicts with this file, **this file wins**.

---

## Definitions

### MarketSnapshot
An immutable record of market inputs used for pricing/Greeks.

A MarketSnapshot MUST include:
- timestamp (UTC)
- underlying quote (bid/ask/mark/last per policy)
- option chain slice used (bid/ask/mark/last/iv where available)
- any model inputs required by `ModelConfig` (rates/div/borrow if used)

Snapshots are identified by a stable ID/hash and are replayable.

---

## Live Mode (default)

Live Mode means:
- the system continuously refreshes market data from Schwab
- each refresh produces a **new immutable MarketSnapshot**
- the UI always prices/renders from the **latest snapshot** unless the user pins

### Refresh Cadence (MVP)
- Default refresh cadence: **250 ms** (4 Hz)
- The cadence MUST be configurable
- If requests overlap, the system MUST coalesce to "latest only"
  - do not queue a backlog
  - skip intermediate updates if necessary

Rationale:
- fast enough to feel real-time
- slow enough to avoid hammering APIs
- supports deterministic “latest snapshot” behavior

---

## Pinned Mode

Pinned Mode means:
- the current snapshot is selected and **frozen**
- all pricing/Greeks/curves/tables must use the pinned snapshot ID
- no background refresh may change the pinned snapshot

Pinning MUST persist:
- snapshot ID
- timestamp
- symbol
- a minimal human-readable label (optional)

Unpinning returns the view to Live Mode (latest snapshot).

---

## UI Responsiveness Rule

Crosshair movement MUST NOT trigger recomputation against Schwab.

Crosshair interaction must use:
- cached arrays / matrices computed from the current snapshot
- interpolation / lookup only

If a recompute is required due to changing inputs, it must be triggered by:
- a new snapshot (live refresh), or
- an explicit user action (change scenario / change trade / change config)

---

## Failure Behavior

If Schwab fetch fails:
- keep the last good snapshot as “latest”
- surface an explicit error state
- do not fabricate quotes or IV values
