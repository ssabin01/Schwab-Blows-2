USER_FLOWS.md

# User Flows — AegisRisk

## Flow 1: Start compare session
1. Open Compare Workspace.
2. Select active trade target: A or B (one is “armed” for edits).
3. Choose scenario mode: Curves or Matrix.
4. Charts + tables render for both trades (empty trades show zeroed outputs and clear “no legs” state).

## Flow 2: Build a trade from live option chain (single-leg)
1. Enter underlying symbol (search).
2. Load chain for selected expiry (default nearest weekly/monthly; user can change).
3. Click:
   - ask cell → adds a buy leg to active trade
   - bid cell → adds a sell leg to active trade
4. System creates/updates a MarketSnapshot (live) and triggers recompute per recompute policy.

## Flow 3: Build a multi-leg structure from chain (Control mode, macOS)
1. Hold Control key → UI enters multi-add mode (visible indicator).
2. Click multiple bid/ask cells across strikes/expiries as allowed by UI filter.
3. Each click adds a leg immediately to active trade without leaving the chain.
4. Release Control (or click “Done”) → ends build session.
5. Recompute:
   - If auto-recompute: debounce and compute once at end-of-session.
   - If manual: show “Recompute” pending state.

## Flow 4: Edit trade after building
1. In Positions/legs table:
   - change qty
   - edit entry price
   - delete leg
2. Toggle include/exclude checkbox per leg.
3. Charts and tables update deterministically with clear stale/dirty indicators if compute is pending.

## Flow 5: Compare under shared scenario controls
1. In global control bar:
   - set horizon curves (explicit days list or N@step)
   - set spot range and resolution
   - toggle snap/interp
2. Both trades re-render under identical scenario definitions.
3. A–B diff is displayed in tables and (optionally) as overlay.

## Flow 6: Inspect with crosshair (curves)
1. Move cursor over any chart.
2. Crosshair syncs across:
   - Trade A + Trade B
   - primary chart + value + all greeks
3. Readouts show A, B, and A–B at the same spot and horizon.

## Flow 7: Inspect with cell selection (matrix)
1. Click a cell in either matrix.
2. Selection syncs across A and B matrices (and optional diff matrix).
3. “Live” row in Price Slices reflects selected cell’s spot and vol shock.

## Flow 8: Pin snapshot for reproducibility
1. Click “Pin snapshot”.
2. UI labels the session as pinned; the snapshot id/hash becomes part of all result metadata.
3. Re-opening the pinned snapshot reproduces analytics within tolerance.

## Flow 9: Import positions (optional in MVP)
1. Authenticate read-only provider.
2. Select account positions.
3. Map positions into Trade A or B (as legs).
4. Evaluate and compare as usual.