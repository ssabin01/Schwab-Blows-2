# Analytics Spec — AegisRisk

## 1. Core contract
Given identical:
- Trade (same legs and entry inputs)
- MarketSnapshot (same observed inputs)
- ScenarioGrid (same grid definition)
- ModelConfig (same methods and conventions)

The engine must produce identical outputs within explicit tolerances.

## 2. Inputs

### 2.1 MarketSnapshot fields (minimum)
- Underlying:
  - symbol
  - spot price (mid/last per policy)
  - timestamp(s)
- Options (per contract):
  - bid, ask (required for chain-driven entry inference)
  - mark/mid (optional but recommended)
  - implied vol (optional; required if RAW_CHAIN_IV is used)
  - timestamp(s)
- Rates/dividends:
  - risk-free rate input (can be flat for MVP; must be explicit)
  - dividend/borrow yield (explicit; can default to 0 for MVP but must be recorded)

All missing inputs must be handled via explicit warnings and fallback policies.

### 2.2 Trade and leg conventions
- Option leg includes:
  - underlying symbol
  - expiry (timestamp/date)
  - strike
  - right (call/put)
  - style (American/European if known; default equity options assumed American unless provider states otherwise)
  - contract multiplier (e.g., 100 for standard equity options; must come from instrument metadata)
  - signed quantity (positive long, negative short)
  - entry price (user-editable)
  - fees/commission (configurable)
- Stock leg:
  - symbol
  - signed shares
  - entry price
  - fees

## 3. Measures

### 3.1 Value
Net theoretical value of the trade under the scenario state:
- Value = sum(leg_value) - fees_if_configured

### 3.2 P/L Open
P/L Open at scenario state:
- P/L Open = Value(state) - Value(entry_context)
Entry context is defined by entry prices and fees for each leg:
- Option leg entry value = entry_price * multiplier * qty_signed
- Stock leg entry value = entry_price * shares_signed

Fees policy must be explicit in ModelConfig.

### 3.3 Greeks
Minimum set:
- Delta, Gamma, Theta, Vega
Output conventions:
- Delta: per 1.00 change in underlying price (currency per $1 move for a 1-contract position when multiplied appropriately)
- Gamma: per 1.00 change in underlying price
- Vega: per 1.00 change in volatility (i.e., vol from 0.20 to 0.21 is +0.01; UI may also display per 1 vol-point = 0.01)
- Theta: reported per calendar day by default
  - Theta_day = Theta_year / 365 using ACT/365F unless configured otherwise

## 4. Pricing backends (required behavior)
The engine must support pricing the instruments present in MVP:
- Equity stock legs (linear)
- Equity options (typically American-style)

ModelConfig must declare:
- pricing_method for options:
  - European: Black–Scholes (analytic)
  - American: must use an explicit method (examples: binomial tree, approximation method)
- greeks_method:
  - analytic where available
  - numerical bump where required (with explicit bump sizes recorded)

If American option method is approximation-based, this must be labeled in result metadata.

## 5. Scenario grids

### 5.1 Spot × Time (Curves)
Inputs:
- spot axis: defined as absolute range or % range around current spot with N points
- time axis: list of horizons (days) or generated as N curves @ step
- include expiry toggle: adds a curve at each leg expiry (or nearest supported)

Output:
- For each horizon: arrays over spot grid for Value, P/L Open, Greeks

### 5.2 Spot × Vol (Matrix)
Inputs:
- spot axis as above
- vol axis: list of vol shocks
  - default interpretation: absolute vol points (e.g., +0.05)
  - optional: relative % change
- clamps:
  - effective_vol = max(vol_floor, base_vol + shock) with floor >= 0

Output:
- For each trade and measure: 2D matrix [spot_i][vol_j]
- A–B matrix difference must be supported

## 6. Volatility input modes

### 6.1 RAW_CHAIN_IV (MVP baseline)
- Use per-contract IV if available.
- If contract IV missing:
  - fallback policy must be explicit (e.g., nearest strike IV, nearest neighbor, or error)
- Record data availability and fallbacks in diagnostics.

### 6.2 FITTED_SURFACE (post-MVP hardening)
- Fit method + objective + constraints must be explicit.
- Must run static arbitrage checks:
  - butterfly checks within maturity
  - calendar checks across maturities
- Fail-closed policy must be explicit:
  - fallback to RAW_CHAIN_IV, or
  - fail evaluation with error

## 7. PnL Attribution
Attribution explains value change between:
- base state (anchor)
- compare state (cursor/cell selection)

Method (MVP):
- “Taylor 2nd-order + residual”
Components:
- Actual PnL
- Delta PnL
- Gamma PnL
- Vega PnL
- Theta PnL
- Explained total
- Residual

Reconciliation:
- actual ≈ explained + residual within tolerance
- leg sums reconcile to trade totals within tolerance

## 8. Error handling
- No silent NaNs.
- Every computation returns:
  - value arrays/matrices (if successful)
  - warnings list
  - error list (if failed)
UI must surface warnings/errors clearly.
