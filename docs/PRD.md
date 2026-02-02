# PRD — AegisRisk

## 1. Problem
Trade comparison is slow and error-prone when users must manually synchronize scenario settings, axes, horizons, and readouts across multiple views. Most tools make “A vs B” a multi-step chore.

## 2. Goal
Make A vs B comparison instantaneous under one global scenario definition, with synchronized inspection and diff-first output across charts, tables, and attribution.

## 3. Users
- Options traders iterating on structures quickly
- PM/risk users needing “what happened” and “why” (attribution)

## 4. MVP deliverables
### 4.1 Compare Workspace
- Trade A and Trade B side-by-side with swap.
- One global control bar drives both trades (scenario mode, horizon/curves, axes, measure, snap/interp).

### 4.2 Live chain → trade builder (MVP scope change)
A built-in chain view is required in MVP to create/edit Trade A and Trade B without importing positions.

Requirements:
- Symbol lookup → load option chain.
- Chain rows show strikes; columns show bid/ask (and optionally mark/IV/volume/OI).
- Click interactions:
  - Click ask cell: add a buy-to-open simulated option leg to the currently active trade (A or B).
  - Click bid cell: add a sell-to-open simulated option leg to the active trade.
  - Holding Control (macOS) turns clicks into “multi-add mode”:
    - each click adds a leg without leaving the chain
    - exiting multi-add mode ends the build session (and triggers recompute behavior per settings)
- Default entry price rule:
  - ask click uses ask as entry for buy legs
  - bid click uses bid as entry for sell legs
  - entry is editable after creation
- Quantities default to 1 contract unless user changes a “default qty” control.
- The chain is strictly a builder; it must not call order endpoints or produce routable orders.

### 4.3 Analytics + UX
- Deterministic MarketSnapshot creation from live chain/quotes.
- Spot × Time (curves) and Spot × Vol (matrix) scenario evaluation.
- Charts per trade:
  - Primary measure chart (selected)
  - Value chart (always visible)
  - Greeks strip (Δ, Γ, Θ, ν) always visible
- Crosshair/cell selection synchronized across both trades and all charts/matrices.
- Tables:
  - Price Slices (with a Live row)
  - Positions/legs with include/exclude
  - PnL Attribution (Taylor 2nd-order + residual)

## 5. Non-goals (MVP)
- Execution/routing
- Advanced portfolio aggregation across many strategies
- Full clone of any existing platform

## 6. Product requirements source of truth
This PRD describes product intent. The functional requirements and acceptance criteria live in the consolidated requirements spec (add it to the repo as `/docs/REQUIREMENTS.md`).

## 7. Release criteria (MVP)
- Can build both trades from live chain clicks (including multi-leg Control mode)
- Can run both scenario types with synchronized inspection and diff outputs
- Determinism: pinned snapshot + fixed config reproduces outputs within tolerance
- No NaNs leak to UI; explicit errors/warnings only