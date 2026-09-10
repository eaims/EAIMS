# EAIMS 1.0.1 — Validation and Review Hardening

EAIMS 1.0.1 is a corrective software and documentation release for the 1.0 reference implementation. It preserves the frozen normative specification and existing valid synthetic reference results.

## Corrections

- Reject evidence with empty or missing collection timestamps and ambiguous executable field types before assessment.
- Reject non-finite numbers, recursive/non-JSON input and duplicate YAML keys.
- Prevent duplicate review IDs and finding keys from silently replacing findings, including blockers.
- Preserve the original review ledger when applying resolution records.
- Resolve installed review schemas through the same package data root as the assessment engine.
- Add `review summarize --fail-on-unmet`: write reports and exit 1 when review exit criteria remain unmet; malformed review input exits 2.

## Integration and documentation

- Dedicated v1 fixture and result JSON Schemas.
- A complete v1 assessment quickstart, report interpretation and review automation guide.
- Clear legacy labels on v0.2.x questionnaire, scoring, conceptual crosswalk and browser resources.
- Consistent 1.0.1 package, runtime, citation and container image versions.

## Validation

The hardening baseline passed 229 tests and retained all three golden reference results. Release validation also checks metadata consistency and the installed package, dependency audit, SBOM, Docker and Compose execution. Publication is gated on successful CI for the exact release commit. The attached wheel is the artifact built and installation-tested by that CI run; SHA256SUMS records its checksum.

## Upgrade

Install the attached `eaims-1.0.1-py3-none-any.whl`, or install from a checkout of tag `v1.0.1`:

```bash
python -m pip install --upgrade ./eaims-1.0.1-py3-none-any.whl
```

Previously accepted malformed inputs may now be rejected. Replace quoted boolean strings with booleans, quote timezone-aware timestamp strings, use finite nonnegative numeric financial values, remove duplicate identifiers and supply unique YAML keys. Review report generation retains its previous success exit code unless `--fail-on-unmet` is requested.

The v0.2.x commands and schemas remain available. No migration of valid v1 reference inputs is required. Package/release version `1.0.1` and normative provenance `1.0.0-fc16` intentionally differ; this patch does not redefine the maturity model.

## Evidence boundary

EAIMS remains field-informed rather than field-validated. Passing software checks does not establish empirical validity, accredited certification, regulatory conformity, production control effectiveness or completion of independent external review. The three reference implementations are synthetic.

Author and founding steward: Elias Naserkhaki.
