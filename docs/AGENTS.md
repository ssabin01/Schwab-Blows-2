# AegisRisk — AGENTS.md (repo root)

## Source of truth (read these first)
- /docs/REQUIREMENTS.md
- /docs/MVP_SCOPE.md
- /docs/ARCHITECTURE.md
- /docs/API_CONTRACT.md
- /docs/ANALYTICS_SPEC.md
- /docs/VALIDATION_CASES.md
- /docs/BACKLOG.md
- /docs/STATE.md

## Hard constraints (non-negotiable)
- Decision engine only: NO order routing, NO execution, NO OMS/EMS.
- Determinism: analytics must be reproducible from snapshot_id/hash + trade hash + scenario grid hash + model config hash.
- Never silently return NaNs. Return explicit errors/warnings.

## How to work in this repo
1. RECON: Identify relevant files and any missing info.
2. PLAN: Propose a small PR-sized plan (1 backlog item max).
3. IMPLEMENT: Make changes + add tests.
4. VERIFY: Run the repo’s standard commands (below). If they don’t exist yet, create them as part of bootstrap.
5. HANDOFF: Update /docs/STATE.md with what changed, what’s next, and open decisions.

## Standard commands (Codex must run these before finishing)
- make setup
- make lint
- make test

If Makefile does not exist yet, create it and wire these commands to the project’s actual tooling.

## PR requirements
- Include tests for new logic (especially analytics + hashing).
- Update docs when behavior changes (at minimum /docs/STATE.md).
