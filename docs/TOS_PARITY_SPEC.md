# ToS Analyze Tab Numeric Parity Specification

## Purpose

This document defines the **numeric parity contract** for **implied volatility (IV)** and **Greeks** relative to the **thinkorswim Analyze tab** (“ToS”).

When `ModelConfig.mode = TOS_PARITY`, all IV and Greek outputs **must numerically match thinkorswim Analyze tab results** within defined tolerances, given identical inputs and settings.

This document is **authoritative** for IV and Greek calculations.  
If any other document conflicts with this one, **this document wins**.

---

## 1. Priority Order (Non-Negotiable)

1. **Accuracy is paramount**
   - Numeric parity with thinkorswim Analyze tab is the primary objective.
2. **Speed is secondary**
   - Slower computation is acceptable if required for correctness.
3. **Zero-latency UI is tertiary**
   - UI may be ugly; responsiveness optimizations must not change numeric outputs.

---

## 2. Scope of Parity

### Included
- Implied Volatility (IV)
- Greeks:
  - Delta
  - Gamma
  - Vega
  - Theta
  - Rho (if applicable for the instrument)

### Explicitly Excluded
- UI styling or appearance
- Chart rendering details
- Order routing or execution
- Any non-Analyze-tab features

---

## 3. Pricing Model Mapping (Locked)

| Instrument Type | Pricing Model |
|-----------------|---------------|
| European options | Black–Scholes (analytic) |
| American options | Bjerksund–Stensland (ToS-style approximation) |

Rules:
- No alternative pricing models are permitted in `TOS_PARITY` mode.
- Approximations must be labeled in output metadata.

---

## 4. Canonical Price Inputs

Unless contradicted by future ToS validation fixtures:

- **Underlying price:** bid/ask midpoint (“mark”)
- **Option price for IV inversion:** bid/ask midpoint (“mark”)

If bid/ask is unavailable:
- **Fail closed** with explicit error.
- No silent substitution with last trade or theoretical price.

---

## 5. Volatility Mode (MVP)

- **Volatility mode:** `RAW_CHAIN_IV`
- **Source:** Schwab-provided per-contract IV where available.

### Missing IV Policy (Explicit)

Default behavior in `TOS_PARITY` mode:

> **FAIL**
>
> If contract IV is missing, calculations must error with a clear diagnostic.

Optional override (must be explicitly set in `ModelConfig`):
- `NEAREST_STRIKE` (same expiry, same option right only)

No other fallbacks are allowed.

---

## 6. Rates, Dividends, and Borrow Assumptions (Locked)

The following conventions apply in `TOS_PARITY` mode and reflect standard
hedge-fund risk system defaults as well as thinkorswim behavior.

### Risk-Free Rate (r)
- Single scalar input
- Continuously compounded
- Flat across maturities for MVP
- Default source equivalent to OIS / SOFR
- User-override permitted, but must be explicit

### Dividends (q)
- Modeled as a **continuous dividend yield**
- Discrete dividend schedules are **not** assumed
- Discrete dividends are only used if explicitly supplied
- No dividend inference or projection is permitted

### Borrow / Financing
- Modeled separately from dividend yield
- Default value = 0
- Must be explicitly supplied to take effect

All values must:
- Be recorded in `ModelConfig`
- Be hashed into the run identifier
- Be persisted for audit and replay


To mirror thinkorswim behavior:

- **Risk-free rate (r):**
  - Single scalar input.
  - User-supplied or system default.
- **Dividends (q):**
  - Continuous dividend yield by default.
  - Discrete dividend schedules only if explicitly supplied.
- **Borrow cost:**
  - Separate from dividend yield.
  - Defaults to zero unless explicitly set.

All values must:
- Be recorded in `ModelConfig`
- Be hashed into the run identifier
- Be persisted for audit and replay

---

## 7. Time and Day Count Conventions

- **Time to expiration:** calendar time
- **Day count basis:** ACT/365F
- **Theta:** reported per calendar day

These conventions are fixed in `TOS_PARITY` mode.

---

## 8. Pricing and Solver Requirements (Locked)

### European Options
- Analytic Black–Scholes formula

### American Options
- Bjerksund–Stensland (2002) approximation
- No lattice, PDE, or alternative methods permitted in `TOS_PARITY` mode
- Approximation usage must be labeled in metadata

### Implied Volatility Solver
- Deterministic, bracketed root-finding solver (e.g., Brent)
- Fixed parameters:
  - Absolute IV tolerance: 1e-6
  - Maximum iterations: ≥ 100
- No adaptive heuristics
- No stochastic behavior
- Same inputs must always produce identical outputs

### Failure Behavior
- Solver non-convergence is a **hard error**
- Missing inputs are **hard errors**
- No silent fallback or smoothing is permitted

## 9. Greek Computation Rules

- Greeks must be computed **from the pricing model**, not from finite differences on market price.
- If finite differences are required internally:
  - Step sizes must be fixed and documented.
- All Greeks must be computed at the **same implied volatility** used to match ToS price parity.

---

## 10. Validation and Acceptance Criteria

### Golden Test Fixtures

Parity is validated using **ToS-derived golden fixtures**.

Each fixture must include:
- Timestamp
- Underlying snapshot
- Option contract identifiers
- thinkorswim Analyze tab settings
- thinkorswim IV and Greeks
- Expected outputs and tolerances

### Initial Numeric Tolerances

- **IV:** ±0.01 volatility points
- **Greeks:** ±0.1% relative error or explicit absolute thresholds per Greek

Failure to meet tolerance is a **test failure**.

---

## 11. Auditability and Reproducibility

Every parity run must persist:
- Raw Schwab API inputs
- Normalized `MarketSnapshot`
- `ModelConfig` (fully expanded)
- Pricing backend version and solver version

Given identical inputs, the system **must reproduce identical outputs**.

---

## 12. Explicit Non-Goals

- Matching undocumented thinkorswim bugs
- Artificial smoothing or stabilization beyond ToS behavior
- UI optimizations that alter numeric results
