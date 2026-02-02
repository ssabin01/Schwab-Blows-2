# Validation Cases — AegisRisk

This file defines golden cases and invariants. Numeric cases below use standard Black–Scholes with ACT/365F.

## 1. Determinism
### Case D-1: Same inputs → same outputs
Given:
- same MarketSnapshot (pinned)
- same TradeVersion
- same ScenarioGrid
- same ModelConfig

Then:
- arrays/matrices match within tolerance (recommend: abs <= 1e-9, rel <= 1e-9 for pure BS; wider for tree methods)

## 2. Black–Scholes numeric goldens (European)

Conventions:
- S spot, K strike, r risk-free, q dividend yield, σ vol, T year-fraction
- Vega is per 1.00 vol unit (e.g., 0.20 → 0.21 is +0.01)
- Theta_day = Theta_year / 365

### Case BS-1 (ATM, 30d)
Inputs:
- S=100
- K=100
- r=0.05
- q=0.00
- σ=0.20
- T=30/365

Expected (tolerance: 1e-6):
- Call price: 2.4933768194
- Put price:  2.0832611958
- Call delta: 0.5399635456
- Put delta: -0.4600364544
- Gamma:      0.0692276405
- Vega:       11.3798861044
- Call theta (per day): -0.0449881561
- Put theta  (per day): -0.0313457062

### Case BS-2 (OTM call, div yield, 0.5y)
Inputs:
- S=100
- K=110
- r=0.03
- q=0.01
- σ=0.25
- T=0.5

Expected (tolerance: 1e-6):
- Call price: 3.7230100452
- Put price:  12.5840754823
- Call delta: 0.3449878381
- Put delta:  -0.6500246411
- Gamma:      0.0207764082
- Vega:       25.9705102708
- Call theta (per day): -0.0193723642
- Put theta  (per day): -0.0131919343

## 3. American option invariants (tree method)

If using a CRR binomial tree with N=200 steps for this test:

### Case AM-1: Non-dividend call early exercise should not add value (invariant)
Inputs:
- Same as BS-1
Expected:
- American call price equals European call price within 1e-3
- (Binomial Euro ~ 2.4905182527, Binomial Amer ~ 2.4905182527)

### Case AM-2: American put should be >= European put
Inputs:
- Same as BS-1
Expected:
- American put >= European put
- Example with N=200:
  - Binomial Euro put ~ 2.0804026291
  - Binomial Amer put ~ 2.1115903094

## 4. Trade aggregation tests
### Case T-1: Two identical legs sum linearly
- Build trade with two identical long call legs (same contract, qty=1 each).
Expected:
- Value and Greeks equal 2x single-leg outputs across all scenario states.

### Case T-2: Long + short cancels
- One long call qty=1 and one short call qty=-1 same contract.
Expected:
- Value and Greeks are ~0 across the grid (fees excluded).

## 5. Scenario grid tests
### Case SG-1: T+0 required
- Generate horizons with N@step that doesn’t explicitly include 0.
Expected:
- Engine inserts T+0 by default unless explicitly disabled.

### Case SG-2: Vol clamps
- Base vol 0.10, apply shock -0.50 with floor 0.00
Expected:
- effective vol used is 0.00 and warning emitted.

## 6. P/L Open tests
### Case PL-1: Entry = model value → P/L Open ~ 0 at T+0
- For a European option priced by BS:
  - set entry price equal to model mid price at T+0
Expected:
- P/L Open at T+0 is ~0 (fees excluded)

## 7. Attribution tests
### Case PA-1: Reconciliation
Expected:
- actual_pnl ≈ explained_total + residual
- leg component sums ≈ trade component totals
Tolerance:
- configurable; recommend 1e-6 for analytic-only; wider for approximations.

## 8. Chain click → trade builder tests (UI/service integration)
### Case UI-1: Ask click creates buy leg
- Click ask for a contract in chain.
Expected:
- leg side = long
- entry price = ask observed at click time
- leg added to active trade (A or B)

### Case UI-2: Bid click creates sell leg
Expected:
- leg side = short
- entry price = bid observed at click time

### Case UI-3: Control multi-add session accumulates legs
Expected:
- multiple clicks create multiple legs
- recompute occurs once at end of session if using debounce policy
