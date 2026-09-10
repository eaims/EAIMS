# FC16 → Existing Repository Merge Map

FC16 is a release-candidate work tree, not a root-level replacement archive.

| FC16 path | Merge treatment |
|---|---|
| `spec/` | Add as v1 canonical structured specification; review against existing normative docs. |
| `src/eaims/` | Reconcile with current executable engine; preserve backward-history through Git, not duplicate legacy code silently. |
| `tests/` | Merge; retain existing v0.2 regression tests where still useful and clearly version-scope them. |
| `schemas/` | Merge and version schemas explicitly. |
| `reference-implementations/` | Add as synthetic v1 reference cases. |
| `review/` | Add reviewer package/workflow. |
| `validation/` | Add generated/retained validation artifacts; do not claim hosted runtime evidence until CI produces it. |
| `research/` | Merge evolution report without deleting existing research assets. |
| `.github/workflows/validate.yml` | Reconcile with existing workflows; do not remove DCO/security/release workflows. |
| `README.md` | Manually compose a v1 README using existing origin, license, governance, disclaimer and project links. Do not blind-replace. |
| `pyproject.toml` | Reconcile command/API compatibility with current package before merge. |
| Docker files | Reconcile current local/browser container behavior with FC16 validation services. |

Legal/IP/governance files are now intentionally included in the local v1.0 candidate as reviewed replacement text. On a future authorized release-branch integration, apply these reviewed versions deliberately rather than preserving older conflicting copies. Preserve unrelated historical/security/community assets unless separately reviewed. The v1 license map remains CC BY 4.0 for documentation/specification/assessment content and Apache-2.0 for code/tests/workflows/JSON Schemas and other executable configuration, with the detailed boundary in `LICENSE`.

## Explicit compatibility gate

The current live package identity is `eaims` and its v0.2.1 CLI exposes `validate`, `score`, and `report`. FC16 preserves those commands through regression-tested compatibility code. During merge, retain the existing public `scoring.py` and `reporting.py` modules as versioned legacy APIs. See `integration/COMPATIBILITY-GATE.md`.


## Non-negotiable public Python API preservation

During any future authorized merge, the existing public Python API modules `src/eaims/scoring.py` and `src/eaims/reporting.py` SHALL be preserved and reconciled deliberately. They MUST NOT be deleted, overwritten blindly, or lost through bulk directory replacement. Existing downstream imports and v0.2.1 behavior must remain version-scoped and regression-tested while v1 functionality is introduced alongside them.

Bulk replacement of `src/eaims/` is prohibited. The merge must be path-by-path/diff-based, with explicit compatibility review for `scoring.py`, `reporting.py`, CLI routing, package exports, schemas, and tests.
