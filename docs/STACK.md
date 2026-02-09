# Stack Decision (MVP)

This document locks the **implementation stack** for the MVP.

If any other document or instruction conflicts with this file, **this file wins**.

---

## Priority Order

1. **Accuracy is paramount**
2. **Speed is secondary**
3. **Zero-latency interaction is tertiary**
4. UI aesthetics are irrelevant

All stack choices are made to optimize for this order.

---

## Chosen Stack

### Application Model
- **Desktop-first**
- Single-process where possible
- No client/server split for MVP

Rationale:
- Eliminates network latency
- Eliminates IPC overhead
- Guarantees lowest possible jitter for interactive risk inspection

---

### Programming Language
- **Rust**

Rationale:
- Deterministic numerical behavior
- No garbage collector in hot paths
- Strong typing for financial correctness
- Single language across compute, ingestion, and UI backend

---

### UI Framework
- **Tauri (Rust backend + embedded webview)**

Rationale:
- Native performance characteristics
- Direct access to Rust compute layer
- Minimal overhead compared to browser-based apps

---

### Rendering / Charts
- **Canvas or WebGL**
- No SVG or DOM-based charting libraries

Rationale:
- Crosshair movement must never block
- Rendering must be decoupled from computation
- Pixel-level control preferred over declarative charting

---

### Pricing & Risk Engine
- **Rust implementation**
- Deterministic math only
- No dynamic code loading
- No scripting languages in the compute path

Rationale:
- Ensures stable IV/Greeks under rapid updates
- Avoids runtime jitter and GC pauses
- Simplifies audit and reproducibility

---

### Market Data Ingestion
- **Rust HTTP client**
- Schwab API behind a strict adapter boundary
- Snapshot-based ingestion model

Rationale:
- External data sources are not trusted directly
- All inputs must be normalized and snapshotted
- Deterministic replay is required

---

### Storage
- **SQLite (local-first)**

Optional (later):
- Parquet for bulk historical snapshots

Rationale:
- Simple, deterministic, portable
- Zero operational complexity for MVP
- Suitable for audit trails and replay

---

### Testing
- Rust unit tests
- Determinism tests (same inputs → same outputs)
- Golden fixture support (for future ToS parity validation)

Rationale:
- Numeric drift must be detectable
- Regression must be caught automatically

---

### Build & Tooling
- `cargo` as the source of truth
- `justfile` or `make` for common commands

Required commands:
- `dev`
- `test`
- `lint`
- `build`

---

## Explicit Non-Goals

- Web-first deployment
- Microservices
- Distributed compute
- Python, JS, or JVM-based pricing engines
- UI polish or theming

---

## Summary

This stack is intentionally:
- Boring
- Deterministic
- Fast
- Auditable

It is chosen to support **hedge-fund-grade risk analysis**, not consumer UX.

Any deviation from this stack requires an explicit ADR.
