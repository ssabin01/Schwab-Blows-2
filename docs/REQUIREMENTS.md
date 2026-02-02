# AegisRisk — Complete Requirements

## 0) Document status and scope

This document is the consolidated, end-to-end requirements specification for **AegisRisk**, a hedge-fund-grade (math-first, deterministic, auditable) **trade comparison and risk workbench** focused on eliminating friction in side-by-side strategy comparison.

* **Decision engine only**: no order routing, no trade execution, no OMS/EMS.
* **Primary integration**: Schwab API for read-only account/position and market data ingestion (exact endpoints/scopes depend on Schwab approvals and entitlements).
* **UI goal**: terminal-grade (Bloomberg-like), keyboard-forward; polish is secondary to correctness and speed.

---

## 1) Problem statement

Existing retail tools make side-by-side comparison of two trades slow and error-prone due to:

* Excess setup steps (simulated trade scaffolding, window detaching, manual selection).
* Manual synchronization burden (axes, scenario settings, curve sets).
* Poor comparative inspection (crosshair not synchronized; difficulty reading matching points).

AegisRisk must enable:

* **Instant A vs B comparison** under **one global scenario definition**.
* **Global lockstep controls** across both trades and all subordinate charts.
* **Synchronized inspection** (crosshair and readouts) and **diff-first** output (A–B).

---

## 2) Product objectives

### 2.1 Primary objective (MVP)

Provide a **Compare Workspace** that:

* Loads Trade A and Trade B (from imported positions or locally-defined simulated trades).
* Shows side-by-side **P/L**, **Value**, and **Greeks** with identical horizon curve sets.
* Provides tables comparable to thinkorswim Analyze (SS2) for:

  * price slices metrics
  * positions/legs with checkboxes
  * PnL attribution (explained PnL)

### 2.2 Secondary objectives (MVP)

* Deterministic analytics with reproducible snapshots.
* Low-latency interactions (cursor, toggles, scenario changes).
* Explicit, versioned model configuration and diagnostics (especially vol surface).

---

## 3) Users and use-cases

### 3.1 Primary users

* Options traders comparing trades (two or more) quickly.
* PMs and risk analysts who need “what” and “why” (PnL attribution and stress matrices).

### 3.2 Core use-cases

1. Compare two trades at the same measure and scenario, instantly see differences.
2. Move the cursor and read A, B, and A–B at the exact same spot/horizon.
3. Switch horizon mode (e.g., N curves @ day step) once; everything stays in sync.
4. Inspect Greeks visually below each trade (same horizons as P/L and Value).
5. Create price slices and compare metrics in a table (like SS2).
6. Toggle legs on/off via checkboxes; edit trades by adding/removing legs; recompute.

---

## 4) Non-goals

* No execution/routing.
* No attempt to clone all thinkorswim functionality.
* No autonomous trading.

---

## 5) Core product concepts and definitions

### 5.1 Trade (Strategy)

A Trade is a collection of legs (stock and/or options) with:

* quantities, sides, contract specifications, entry inputs, fees
* editable (via TradeDraft) and versioned for reproducibility

### 5.2 Market snapshot

A MarketSnapshot is a point-in-time set of observed inputs used for evaluation:

* underlying quotes
* option quotes / IVs (as available)
* rates/dividends inputs (per ModelConfig requirements)
* metadata timestamps and provenance

### 5.3 Model configuration

ModelConfig defines:

* pricing backend selection (fast interactive vs high-precision)
* volatility input mode (raw chain vs fitted surface)
* rules for scenario shocks (as applicable)
* conventions (day count, calendars) explicitly

### 5.4 Scenario grid

A ScenarioGrid defines which states to evaluate:

* **Spot × Time (Curves)** mode
* **Spot × Vol (Matrix)** mode (MVP requirement)
  Future: Spot × Vol × Time cube

### 5.5 Measures

At minimum:

* P/L Open
* Value (theoretical/net value)
* Greeks: Delta, Gamma, Theta, Vega
  (Extensible set allowed, but not required for MVP.)

---

## 6) Functional requirements

### 6.1 Compare Workspace (MVP)

**FR-1: Two-trade compare**

* The UI MUST support selecting **Trade A** and **Trade B** and rendering them side-by-side in one workspace.
* Workspace MUST support swap A/B.

**FR-2: Global control bar**

* One global control set MUST drive both trades and all charts:

  * scenario mode selector
  * horizon mode + parameters
  * measure selector (primary chart)
  * price axis range and resolution
  * axis lock toggle

**FR-3: Zero-click syncing**

* No per-panel duplicated controls for scenario/measure/axes in MVP.
* Any change to the scenario definition MUST re-render both trades identically.

---

### 6.2 Charts layout per trade (MVP)

Each trade panel MUST contain stacked charts sharing the same X-axis (underlying spot) and horizon curve set:

**FR-4: Primary chart**

* Shows the selected measure (e.g., P/L Open).

**FR-5: Value chart (always present)**

* A dedicated Value chart MUST be displayed beneath the primary chart (not only as a selectable primary measure).

**FR-6: Greeks strip (always present)**

* Beneath Value, show 4 mini charts:

  * Delta
  * Gamma
  * Theta
  * Vega

**FR-7: Horizon coupling across all charts**

* Horizon curve set MUST be identical across:

  * primary chart User-selected measure
  * value chart
  * all greek charts

---

### 6.3 Horizon mode requirements (MVP)

**FR-8: Supported horizon modes**

* Spot × Time (Curves) MUST support:

  1. explicit horizons (days offsets list)
  2. generated horizons: “N curves @ day step”
  3. include expiry option

**FR-9: T+0 invariant**

* T+0 MUST always exist in the horizon set unless user explicitly disables it.

**FR-10: T+0 visibility**

* T+0 curve MUST be visually distinguishable and must not disappear due to styling defaults.
* Legend MUST support curve isolation (“solo”) to ensure T+0 can be examined even when curves overlap.

---

### 6.4 Crosshair and inspection (MVP) — Fixes for SS1 issues

**FR-11: Full crosshair**

* Charts MUST render a full crosshair:

  * vertical line (X = spot)
  * horizontal line (Y = metric)
  * intersection marker

**FR-12: Crosshair sync**

* Crosshair MUST be synchronized across:

  * Trade A and Trade B
  * primary chart, value chart, and all greek charts

**FR-13: Readability**

* Crosshair MUST be readable on dark background:

  * MUST use a high-contrast rendering method (e.g., halo/outline via two-stroke or equivalent)
  * thickness MUST be configurable (default clearly visible relative to curve strokes)
  * axis readouts MUST show:

    * X spot at bottom axis
    * Y value at right axis

**FR-14: Snap/interp**

* Crosshair MUST support:

  * snap-to-grid ON/OFF
  * interpolation ON/OFF for readouts

---

### 6.5 Metrics tables (MVP) — Replace list-in-box UI

**FR-15: Price Slices table (SS2-style)**

* The product MUST provide a **Price Slices** table similar in function to thinkorswim Analyze (SS2):

  * checkbox per slice to show/hide slice markers on charts
  * a “Live” slice that follows the crosshair spot
  * ability to add/remove additional slices

**FR-16: Price Slices table columns**
At minimum, for the selected readout horizon:

* Spot price / offset
* For Trade A, Trade B, and A–B difference:

  * Delta, Gamma, Theta, Vega
  * P/L Open
  * Value

**FR-17: No boxed lists for metrics**

* Core metrics (price slices and attribution) MUST be presented as tables by default (not lists within boxes as in SS1).

---

### 6.6 Positions and legs table (MVP) — SS2 parity requirement

**FR-18: Positions table with checkboxes**

* The product MUST provide a **Positions and Simulated Trades** table patterned after SS2:

  * leftmost checkbox column to include/exclude legs from analytics
  * grouped display for a trade/strategy and its legs
  * expand/collapse grouping

**FR-19: Rows represent legs**

* Rows MUST represent:

  * stock legs
  * option legs
    with standard fields (as applicable):
* side (LONG/SHORT), qty, symbol, expiry, strike, call/put, entry, mark (optional)

**FR-20: Include/exclude leg updates**

* Toggling a leg checkbox MUST update:

  * P/L and Value curves
  * Greeks
  * metrics tables
    deterministically.

---

### 6.7 Trade editing (MVP)

**FR-21: Add/delete/edit legs**
For each trade (A and B), user MUST be able to:

* add option leg
* add stock leg
* delete leg
* edit qty/side/entry inputs
* (optional) duplicate leg

**FR-22: Recompute behavior**

* Edits MUST trigger recompute with predictable control:

  * either auto-recompute (debounced) or explicit recompute button (or both)
* The system MUST not silently show stale results after edits.

---

## 7) Scenario Grid requirements

### 7.1 Spot × Time (Curves) (MVP)

**SG-1**

* Evaluate selected measures for a spot grid across multiple horizons (curves).

### 7.2 Spot × Vol (Matrix) (MVP)

**SG-2: Matrix mode availability**

* ScenarioGrid MUST support Spot × Vol mode as a first-class scenario type.

**SG-3: Vol shock axis**

* Vol shocks MUST be definable as:

  * absolute vol points (default)
  * relative percent (optional)
* Must include clamps to prevent invalid vols (e.g., negative vol).

**SG-4: Matrix output**

* Must output a 2D matrix per trade:

  * rows: spot grid points (or spot shocks)
  * columns: vol shocks
* Must support A–B matrix difference.

**SG-5: UI rendering**

* In Spot × Vol mode, UI MUST render:

  * side-by-side matrices for A and B, and optionally A–B
  * synchronized cell selection (like crosshair sync for curves)

---

## 8) PnL Attribution requirements (MVP)

### 8.1 Attribution view (MVP)

**PA-1: PnL decomposition**

* The product MUST provide a PnL Attribution view that explains value changes between two states:

  * base state (anchor)
  * compare state (cursor/selection)

**PA-2: Supported components (MVP)**

* Must output:

  * Actual PnL
  * Delta PnL
  * Gamma PnL
  * Vega PnL
  * Theta PnL
  * Explained total
  * Residual (unexplained)

**PA-3: Trade-level and leg-level**

* Must provide:

  * trade aggregate attribution
  * leg breakdown attribution
  * A–B diffs for components

**PA-4: Table format**

* Attribution MUST be presented as a table (not a list-in-box).

### 8.2 Attribution method labeling

**PA-5**

* Attribution MUST explicitly label the method used:

  * “Taylor 2nd-order + residual” for MVP

**PA-6**

* Residual MUST always be displayed (not hidden by default).

---

## 9) Volatility surface requirements (MVP) — Parameterization + arbitrage constraints

### 9.1 Vol input modes

**VS-1**

* The engine MUST support:

  1. RAW_CHAIN_IV mode (baseline)
  2. FITTED_SURFACE mode (institutional mode)

### 9.2 Fitted surface requirements (institutional mode)

**VS-2: Parameterization requirement**

* FITTED_SURFACE MUST have an explicit parameterization method and calibration objective.
* Must include at least one wing-controlled parameterization option (e.g., SVI-style slice parameterization), plus maturity interpolation.

**VS-3: Arbitrage controls**

* FITTED_SURFACE MUST enforce or validate **static arbitrage** at minimum:

  * butterfly arbitrage checks within maturities
  * calendar arbitrage checks across maturities

**VS-4: Diagnostics**

* Surface fit MUST output diagnostics:

  * fit quality metrics (defined by implementation, but must exist)
  * arbitrage checks pass/fail and worst violation locations
  * data universe used (contract counts/filters)

**VS-5: Fail-closed policy**

* If arbitrage checks fail, the system MUST:

  * fail closed with explicit policy behavior:

    * fallback to RAW_CHAIN_IV, or
    * error out
      Policy must be configured in ModelConfig and recorded in results metadata.

**VS-6: UI visibility**

* UI MUST display fitted surface status:

  * PASS
  * FAIL + fallback
  * ERROR
    and allow drilling into diagnostics.

---

## 10) Analytics engine requirements

### 10.1 Determinism and auditability

**AE-1**

* Identical inputs MUST produce identical outputs (within explicit floating tolerances).

**AE-2**

* Every analytics result MUST include metadata:

  * model config version/hash
  * snapshot id/timestamp
  * scenario grid definition/hash
  * vol surface mode and diagnostics status

### 10.2 Measures

**AE-3**

* The engine MUST produce at minimum:

  * value
  * P/L Open
  * delta, gamma, theta, vega
    at trade and leg level (as needed for attribution and tables).

### 10.3 P/L Open

**AE-4**

* P/L Open MUST be computed consistently as value change relative to entry context, net of configured fees/commissions.

### 10.4 Scenario evaluation performance strategy

**AE-5**

* Scenario grids MUST be evaluated in batch form (vectorized where possible).
* Intermediates MUST be cached so switching measure or moving cursor does not trigger full recompute.

### 10.5 Error handling

**AE-6**

* The engine MUST never silently return NaNs; it must:

  * return explicit error states and warnings
  * surface them in UI and in stored results

---

## 11) Data model requirements

### 11.1 Core entities

**DM-1: Instrument**

* symbol, type, multiplier, currency

**DM-2: OptionContract**

* underlying, expiry, strike, right (C/P), style, settlement

**DM-3: Leg**

* instrument reference, signed quantity, side, entry price, fees allocation (optional)

**DM-4: Trade**

* immutable versioned trade definition for reproducible evaluations

**DM-5: TradeDraft (editable)**

* mutable trade used for editing in workspace prior to committing a version

**DM-6: MarketSnapshot**

* timestamped market inputs + provenance metadata

**DM-7: ModelConfig**

* pricing backend id/version
* vol_surface_mode
* vol_surface_config_ref (required if fitted)
* arbitrage policy (fail-closed behavior)
* conventions (day count, calendars)

**DM-8: ScenarioGrid**

* grid_type:

  * SPOT_TIME_CURVES
  * SPOT_VOL_MATRIX
* spot axis
* time axis (required for curves)
* vol axis (required for matrix)

**DM-9: VolSurfaceConfig**

* method, objective, regularization, constraints, interpolation

**DM-10: VolSurfaceDiagnostics**

* fit timestamp, universe description, quality metrics, arbitrage checks, fallback reason

**DM-11: PriceSliceSet**

* includes Live slice and additional user-defined slices (each with checkbox enable)

**DM-12: AnalyticsResult**

* keyed by (trade, snapshot, model config, scenario grid, measure)
* stores arrays/matrices and diagnostics metadata

**DM-13: PnLAttributionRequest / Result**

* stores base state, compare state, method, outputs with components and residuals

---

## 12) UX requirements (complete)

### 12.1 Global controls

* scenario mode selector:

  * Spot × Time (Curves)
  * Spot × Vol (Matrix)
* horizon mode controls for curves:

  * explicit horizons list
  * N curves @ day step
  * include expiry toggle
* axis controls:

  * shared X range (absolute/%), resolution
  * axis lock ON by default
* inspection controls:

  * snap-to-grid
  * interpolation toggle

### 12.2 Two-trade layout

* Two columns: Trade A and Trade B
* Each column contains stacked charts (primary, value, greeks)
* Legends support:

  * toggle horizon curves
  * solo a curve (required for T+0 visibility)
* Bottom area contains tables:

  1. Price Slices table
  2. Positions table (with checkboxes) for A and B
  3. PnL Attribution table (A, B, A–B)

### 12.3 Spot × Vol matrix layout

* Render A matrix and B matrix side-by-side; optional A–B matrix.
* Shared cell selection across matrices.
* “Live” selection maps to current cursor/cell and drives the Price Slices table live row.

---

## 13) Architecture requirements

### 13.1 Components

* UI Client (terminal-style)
* API layer (internal)
* Market Data Service (Schwab adapter + normalization + caching)
* Analytics Service:

  * Scenario Engine (curves + matrix)
  * Pricing/Greeks engine (fast + optional high-precision backend)
  * Vol Surface Service (fit + diagnostics + arbitrage checks)
  * Attribution Engine (PnL decomposition)
* Snapshot Store (local-first; server option later)
* Secrets storage (encrypted)

### 13.2 Caching

* Cache keys MUST include:

  * trade hash (or trade draft version)
  * snapshot id
  * model config hash
  * scenario grid hash
* Cache must support:

  * fast measure toggles
  * low-latency cursor movement readouts

### 13.3 Streaming vs polling

* Schwab streaming market data capability: **Insufficient data to verify** for an official, stable streaming interface requirement in this spec.
* Architecture MUST support snapshot polling as baseline and allow an adapter interface for streaming if/when available.

---

## 14) Security requirements

* OAuth tokens must be encrypted at rest.
* No tokens in logs.
* Audit log must record:

  * data pulls (symbol set, timestamp, adapter)
  * snapshot creation/load
  * model config changes
* Principle of least privilege:

  * read-only behavior enforced by product (no order endpoints used).

---

## 15) Performance requirements (targets)

* Cursor/crosshair move → readout update: smooth interactive performance target (render loop class).
* Measure toggle (cached): sub-100ms class target.
* Scenario change (typical grids): sub-second class target.
* Cold compute: bounded and profiled; must not freeze UI (use asynchronous compute with deterministic caching).

---

## 16) Testing and validation requirements

### 16.1 Determinism

* Fixed snapshot + fixed model config + fixed scenario grid + fixed trade → identical outputs within tolerance.

### 16.2 Surface arbitrage tests

* Must include discrete checks:

  * convexity/butterfly within maturity
  * calendar consistency across maturities
* Must verify fail-closed behavior:

  * fallback to raw chain or explicit error per policy

### 16.3 Attribution reconciliation

* Must satisfy:
  `actual_pnl == explained_total + residual` within tolerance
* Must validate leg sums reconcile to trade totals within tolerance.

### 16.4 UI acceptance tests

* Crosshair has both vertical and horizontal lines.
* Crosshair readable on dark theme (halo/outline present).
* T+0 visible in legend and can be soloed.
* Greeks charts present beneath each trade and follow the same horizons.
* Metrics presented in tables (Price Slices, Attribution).
* Positions table includes checkboxes and toggles legs correctly.
* Add/delete/edit leg updates analytics and tables predictably.

---

## 17) Roadmap (requirements-based milestones)

### Phase 0 — Lock scope and acceptance criteria

* Finalize this requirements document and acceptance tests list.

### Phase 1 — MVP build (Compare-first)

* Schwab adapter (read-only ingestion as permitted)
* Spot × Time curves mode + stacked charts
* Crosshair sync with readability requirements
* Price Slices table (SS2-style)
* Positions table with checkboxes (SS2-style)
* Trade editing (add/delete/edit legs) + recompute controls
* PnL Attribution table (Taylor 2nd-order + residual)

### Phase 2 — Institutional hardening

* FITTED_SURFACE production implementation with arbitrage constraints and diagnostics
* Spot × Vol matrix mode UI + compute acceleration
* Snapshot persistence and replay at scale (team deployment option)

---

## 18) Acceptance criteria summary (MVP must pass)

1. Side-by-side A/B with globally locked controls (measure, horizons, axes).
2. Full crosshair (vertical + horizontal) visible and readable; synced across all charts and both trades.
3. Greeks charts under each trade (Delta/Gamma/Theta/Vega), sharing the same horizon curves as P/L and Value.
4. T+0 curve present and visible; can be isolated via legend.
5. Metrics appear in SS2-style tables (Price Slices; PnL Attribution), not list-in-box.
6. Positions/legs table with checkboxes like SS2; toggles legs and updates analytics.
7. User can add/delete/edit legs for each trade; recompute updates charts and tables without stale states.
