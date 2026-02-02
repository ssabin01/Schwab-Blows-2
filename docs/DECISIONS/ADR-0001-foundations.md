# ADR-0001 — Foundations

## Status
Proposed (accept when repo stack is selected)

## Decisions

### 1) Local-first architecture for MVP
- UI + local services on the same machine.
- Reason: fastest path to deterministic snapshots and low-latency interaction without deployment complexity.

### 2) MarketSnapshot is the only source of truth for analytics
- Analytics never queries “live” directly; it consumes snapshot IDs.
- Live mode is implemented as a snapshot refresh loop that produces successive snapshots; pinning freezes one.

### 3) Chain-click entry inference is deterministic
- Ask click => buy leg with entry=ask at click time
- Bid click => sell leg with entry=bid at click time
- Entry remains user-editable; edits bump TradeDraft revision.

### 4) Theta unit convention
- Store theta_year internally (if convenient), but report theta per calendar day by default.
- Day count basis: ACT/365F unless configured.

### 5) American options must be explicitly supported
- Provider equity options are commonly American-style; pricing backend must declare its method.
- If approximation used, label it in result metadata.

## Consequences
- Requires snapshot store and hashing early.
- Requires clear UI states for live vs pinned.
