# Security — AegisRisk

## Principles
- Least privilege: read-only scopes only
- Encrypt tokens at rest
- Never log tokens or authorization headers
- Explicit audit logging for data pulls, snapshot creation, config changes

## OAuth handling
- Store refresh/access tokens in OS keychain on macOS if possible.
- If not using keychain:
  - encrypt at rest
  - keep encryption key outside repo and outside the same storage location

## Logging rules
- Redact:
  - tokens
  - account identifiers (unless user opts in)
- Analytics logs must not include provider payload dumps by default.

## Local data
- Snapshot persistence must respect provider licensing.
- Provide a “purge local data” option in UI.

## Read-only enforcement
- Provider adapter must not implement order endpoints.
- If provider SDK exposes order methods, they must be unreachable from the app code path and excluded from scopes.
