# Existing v0.2.1 Compatibility Gate

FC16 implements backward-compatible command routing for the public v0.2.1 CLI contract while keeping v1 assessment semantics separate.

The retained legacy commands are:

```text
eaims validate <assessment>
eaims score <assessment>
eaims report <assessment> [--format ...]
```

The v1 executable workflows use distinct commands:

```text
eaims validate-fixture <fixture.yaml>
eaims assess <fixture.yaml>
eaims review ...
```

## Compatibility guarantees in FC16

- v0.2.1 JSON objects are validated and scored only with v0.2.1 semantics.
- v1 YAML fixtures are never silently routed through v0.2.1 scoring.
- Legacy CLI command behavior is covered by executable regression tests.
- The package identity remains `eaims`.

## Release-branch merge requirement

The current public repository also exposes Python modules such as `eaims.scoring` and `eaims.reporting`. Those modules SHALL be preserved during the release-branch merge so downstream imports are not broken merely by introducing v1. The FC16 work tree does not delete those live repository files.

## Dependency change

v0.2.1 is dependency-free at runtime. FC16 adds PyYAML and jsonschema. This change must remain visible in release notes, dependency audit, and SBOM evidence.

## Schema compatibility

v0.2.1 assessment objects SHALL NOT be silently rescored using v1 semantics. Historical scores remain versioned historical results. Migration requires reassessment or an explicit versioned migration procedure.


### Bulk replacement prohibition

`src/eaims/scoring.py` and `src/eaims/reporting.py` are existing public API surfaces. An authorized v1 merge SHALL preserve/reconcile them explicitly and SHALL NOT use a bulk replacement of `src/eaims/` that removes or silently changes those modules. Any intentional compatibility change requires a documented migration path and regression evidence before release approval.
