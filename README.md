# EAIMS — Enterprise AI Maturity Standard

> An open, vendor-neutral, evidence-grounded and executable framework for assessing and improving enterprise AI maturity while governing value, autonomy, accountability and operational risk.

**Version:** 1.0.0
**Status:** Final release
**Documentation and specification content:** CC BY 4.0
**Code, tests, workflows and JSON Schemas:** Apache-2.0

EAIMS 1.0 moves the project from a research-baseline maturity model toward an executable enterprise AI operating and assurance framework. It does not itself confer certification, regulatory conformity, legal compliance or safety assurance.

## Canonical EAIMS 1.0

- **8 dimensions** and **30 capabilities**
- **5 maturity levels** (L1 Initial → L5 Adaptive)
- **150 capability-specific maturity anchors**
- **206 normative and cross-cutting requirements**
- **177 SHALL / SHALL_NOT requirements**, including **80 critical** requirements
- explicit evidence confidence, applicability, assessment quality and multi-assessor semantics
- G0–G3 gate families with rule-based escalation
- Human Accountability Boundaries (HAB), Human Reserved decisions and bounded AI autonomy
- model/system sourcing, external-change exposure and agent permission envelopes
- diagnostics for maturity debt, autonomy debt, assurance gap and drift

A central design principle is that AI maturity is not maximum automation. Mature organizations determine where automation creates value, where human oversight is necessary, and where accountability must remain human.

## Start with EAIMS 1.0

Follow the [v1 assessment guide](docs/ASSESSMENT-V1.md) for installation, a runnable example, output interpretation and review automation. The reference example detects a synthetic agent exceeding its financial authority; the report identifies the breached gates so the assessor can define a corrective action.

The browser interface in `site/`, the questionnaire in `assessment/`, and the `validate`, `score`, `report` commands are **legacy v0.2.x** resources. Use `validate-fixture` and `assess` for v1.0; do not relabel legacy scores as v1 results.

## Executable reference implementation

The Python package validates structured assessments, evaluates evidence and requirements, applies anchor eligibility and gates, produces deterministic results and reports, and supports structured review operations.

```bash
python -m pip install -e '.[test]'
eaims-validate
pytest -q
python tools/prepush_audit.py
```

The published v0.2.1 CLI commands `validate`, `score`, and `report` remain available through the compatibility path. EAIMS 1.0 adds `validate-fixture`, `assess`, and `review`. Existing public Python modules `eaims.scoring` and `eaims.reporting` are preserved for backward compatibility.

## Synthetic reference implementations

Three end-to-end cases exercise different enterprise conditions:

1. **RI-01 — API-Consumed Analytics Assistant:** model sourcing, external-change exposure, evidence retention and material gates.
2. **RI-02 — Enterprise Autonomous Service Agent:** agent permission envelope, financial/action limits, operational suspension, autonomy drift and G3 controls.
3. **RI-03 — High-Impact Decision Support:** Human Reserved decisions, final human authority, recourse, intervention feasibility and G2 controls.

These cases are synthetic and are not presented as customer deployments or empirical validation.

## Docker

The v1 validator uses `Dockerfile.validator` and runs with a least-privilege container profile:

```bash
docker build -f Dockerfile.validator -t eaims/validator:1.0.0 .
docker compose run --rm validator
```

Hosted CI validates the Docker image and both Compose configurations at runtime. See `docs/PACKAGING-AND-RUNTIME-VALIDATION.md` and `VALIDATION.md` for the validation boundary.

## Validation status

EAIMS 1.0 is **field-informed rather than field-validated**. Its design incorporates observations from feasibility assessment, realistic synthetic reference implementations and enterprise pilot-readiness discussions. Formal multi-organization empirical validation, inter-rater reliability research and independent external review remain part of the research agenda.

The `review/` directory provides structured adversarial questions, reviewer guidance, feedback/resolution schemas and executable BLOCKER/MAJOR exit semantics. No claim is made that independent external review has already been completed.

The final release was promoted from `v1.0.0-rc.1` only after hosted validation passed on `main`, including 186 executable tests, wheel build/install validation, dependency vulnerability auditing, CycloneDX SBOM generation, Docker runtime validation, Docker Compose runtime validation and all three synthetic reference implementations.

## Specification provenance

The final public release version is **1.0.0**. The internal normative specification provenance identifier **`1.0.0-fc16`** is intentionally retained in the frozen normative source and generated reference evidence. This preserves traceability to the exact freeze-candidate content that passed RC1 validation; it does not mean the public release remains a release candidate.

## Project status and stewardship

EAIMS was founded and initially authored by **Elias Naserkhaki**, founding steward of **eaims.org**. Governance, contribution rights and licensing boundaries are documented explicitly in [GOVERNANCE.md](GOVERNANCE.md), [IP_POLICY.md](IP_POLICY.md), [CONTRIBUTING.md](CONTRIBUTING.md), [CLA.md](CLA.md), and [COPYRIGHT-ASSIGNMENT.md](COPYRIGHT-ASSIGNMENT.md).

EAIMS is not ISO, IEC, ANSI, a governmental body or an accredited certification scheme. See [DISCLAIMER.md](DISCLAIMER.md) and [TRADEMARK.md](TRADEMARK.md).

## Licensing and provenance

The detailed boundary is defined in [LICENSE](LICENSE): documentation, normative specification/assessment content and machine-readable specification data other than JSON Schemas are licensed under **CC BY 4.0**; code, tests, automation/build assets, Docker/Compose configuration, workflows and JSON Schemas are licensed under **Apache-2.0**. Public licenses do not transfer ownership, trademarks, governance authority or official-release authority.

See [PROVENANCE.md](PROVENANCE.md), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), [LICENSE-CODE.md](LICENSE-CODE.md), and [LICENSE-DOCS.md](LICENSE-DOCS.md).

## Migration and historical resources

The v0.2.1 research baseline remains part of repository history. See [MIGRATION-v0.2.1-to-v1.0.md](MIGRATION-v0.2.1-to-v1.0.md) and [research/EVOLUTION-0.2x-to-1.0.md](research/EVOLUTION-0.2x-to-1.0.md). Existing community, security, publication, RFC, decision and approved-implementation resources remain part of the repository history and project resources.

## Project website

**eaims.org**
