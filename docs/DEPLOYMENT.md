# Deployment — AegisRisk (MVP)

MVP target is a local-first application:
- UI + local services run on the same machine
- local persistence for snapshots/config/results

## Environments
- dev: verbose logs, mock provider optional
- prod-local: packaged app, secure secrets storage

## Build and release
- Produce versioned artifacts with embedded git commit hash.
- Ship with migrations for local DB schema.

## Configuration
- Provider credentials: via env or secure store (never committed)
- Feature flags:
  - provider adapter selection
  - auto-refresh cadence
  - auto vs manual recompute policy

## Rollback
- Since local-first, rollback primarily means:
  - app version rollback
  - schema migration compatibility policy
