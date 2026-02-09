# Validation and Stubbing Policy (MVP)

This document defines what MUST be implemented correctly before UI work
and what MAY be stubbed during early development.

If any other document conflicts with this file, **this file wins**.

---

## Core Principle

Correctness of pricing, IV, and Greeks is mandatory.

UI completeness, visual polish, and data coverage are secondary.

Codex MUST prioritize deterministic math over UI progress.

---

## Must Be Implemented Correctly (Non-Negotiable)

The following components MUST be fully implemented and correct before
any UI feature is considered “done”:

### Pricing and Risk
- Black–Scholes pricing
- Implied volatility inversion using MARK
- Analytic Greeks computed from BS at implied volatility
- Deterministic solver behavior
- Fail-closed error handling

### Determinism
- Same inputs → same outputs
- Stable snapshot IDs
- Stable run IDs
- Persisted inputs for replay

### Snapshot Semantics
- Live vs pinned behavior per `SNAPSHOT_POLICY.md`
- Pricing and UI must never bypass snapshots

---

## Allowed to Be Stubbed (MVP)

The following MAY be stubbed or simplified initially:

### Schwab Integration
- Real Schwab API calls may be replaced with:
  - recorded fixtures
  - mocked HTTP responses
- Field presence (e.g., implied volatility) may vary

### Validation Fixtures
- thinkorswim-based golden fixtures are NOT required initially
- Placeholder fixtures MAY be used for development

### UI
- Layout may be minimal or ugly
- Tables may be plain
- Charts may be basic as long as:
  - crosshair is responsive
  - values reflect correct cached computations

---

## Validation Expectations

### Internal Validation
Codex MUST implement:
- unit tests for BS pricing
- unit tests for IV inversion
- unit tests for Greeks
- determinism tests (repeatability)

### External Validation (Deferred)
thinkorswim numeric parity tests may be added later
and must not block MVP development.

---

## Failure Rules

- Incorrect math is a hard failure
- Silent fallback is prohibited
- Missing data must surface explicit errors
- UI responsiveness must not mask incorrect calculations

---

## Summary

Codex should:
- Build math first
- Build snapshot plumbing second
- Build minimal UI last

Correctness > speed > appearance.
