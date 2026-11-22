# Changelog

## 1.0.0 — 2026-11-22

- Declare the English client, project model, filters, and errors as the stable
  public API.
- Verify the documented read-only filters against the live API.
- Document that the endpoint returns a top-level array and does not currently
  support result pagination beyond `limit`.
- Add Python 3.11–3.14 CI, opt-in live contract tests, and a release workflow
  that validates version/tag consistency.

## 0.1.0 — 2026-11-20

- Initial public SDK release for the Data Innovacion projects API.
- Add a synchronous client, project filters, and English project model mapping.
- Preserve unknown API fields and expose typed transport/response errors.
- Add docs, deterministic tests, type checks, and optional benchmark suites.
