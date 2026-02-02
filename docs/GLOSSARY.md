GLOSSARY.md

# Glossary — AegisRisk

| Term | Meaning in AegisRisk |
|------|-----------------------|
| Trade | A collection of legs (stock and/or options) evaluated together. |
| Trade A / Trade B | The two trades compared side-by-side in the Compare Workspace. |
| Leg | A single position line: stock or a specific option contract with signed quantity and side. |
| Entry price | The reference price used for P/L Open; set by user or inferred from chain click. |
| MarketSnapshot | A timestamped bundle of observed market inputs used for evaluation (quotes, IVs as available, rates/div inputs). |
| Pinned snapshot | A snapshot frozen for reproducibility; analytics must be replayable from it. |
| Live snapshot | A snapshot that refreshes on cadence; not guaranteed reproducible unless pinned. |
| ScenarioGrid | The set of states to evaluate (spot axis + time axis or vol axis). |
| Spot grid | The set of underlying prices evaluated (absolute or % range with resolution). |
| Horizon | A future time point relative to T+0 used for curves. |
| Measure | A value computed over the grid (Value, P/L Open, Greeks). |
| Value | Theoretical value of the trade under the model inputs (net of fees if configured). |
| P/L Open | Value change relative to entry context (entry price/fees). |
| Delta/Gamma/Theta/Vega | Sensitivities; Theta is reported per calendar day by default (see Analytics Spec). |
| RAW_CHAIN_IV | Uses observed IV from chain quotes as vol input (baseline). |
| FITTED_SURFACE | Uses a fitted vol surface with diagnostics and arbitrage checks. |
| Residual | Unexplained portion of PnL after Taylor-based attribution components. |