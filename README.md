# EAIMS — Enterprise AI Maturity Standard

> An open, vendor-neutral, evidence-grounded and executable framework for assessing and improving enterprise AI maturity while governing value, autonomy, accountability and operational risk.

**Version:** 1.0 Freeze Candidate (FC16)
**Status:** Release-candidate preparation / independent review pending
**Documentation and specification content:** CC BY 4.0
**Code, tests, workflows and JSON Schemas:** Apache-2.0

EAIMS 1.0 moves the project from a research-baseline maturity model toward an executable enterprise AI operating and assurance framework. It does not itself confer certification, regulatory conformity, legal compliance or safety assurance.

## Canonical EAIMS 1.0 candidate

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

## Executable reference implementation

The Python package validates structured assessments, evaluates evidence and requirements, applies anchor eligibility and gates, produces deterministic results and reports, and supports structured review operations.

```bash
python -m pip install -e '.[test]'
PYTHONPATH=. python -m src.eaims.validate
PYTHONPATH=. pytest -q
python tools/prepush_audit.py
```

The published v0.2.1 CLI commands `validate`, `score`, and `report` remain available through the compatibility path. EAIMS 1.0 adds `validate-fixture`, `assess`, and `review`. Existing public Python modules `eaims.scoring` and `eaims.reporting` are preserved during the v1 integration.

## Synthetic reference implementations

Three end-to-end cases exercise different enterprise conditions:

1. **RI-01 — API-Consumed Analytics Assistant:** model sourcing, external-change exposure, evidence retention and material gates.
2. **RI-02 — Enterprise Autonomous Service Agent:** agent permission envelope, financial/action limits, operational suspension, autonomy drift and G3 controls.
3. **RI-03 — High-Impact Decision Support:** Human Reserved decisions, final human authority, recourse, intervention feasibility and G2 controls.

These cases are synthetic and are not presented as customer deployments or empirical validation.

## Docker

The existing browser/reference Docker behavior is retained for backward compatibility. The v1 validator uses a separate Dockerfile:

```bash
docker build -f Dockerfile.validator -t eaims/validator:1.0-fc16 .
docker compose run --rm validator
```

See `docs/PACKAGING-AND-RUNTIME-VALIDATION.md` and `VALIDATION.md` for the runtime-validation boundary.

## Independent review and validation status

EAIMS 1.0 is **field-informed rather than field-validated**. Its design incorporates observations from feasibility assessment, realistic synthetic reference implementations and enterprise pilot-readiness discussions. Formal multi-organization empirical validation, inter-rater reliability research and independent review remain part of the research agenda.

The `review/` directory provides structured adversarial questions, reviewer guidance, feedback/resolution schemas and executable BLOCKER/MAJOR exit semantics. No claim is made that independent review has already been completed.

## Project status and stewardship

EAIMS was founded and initially authored by **Elias Naserkhaki**, founding steward of **eaims.org**. Governance, contribution rights and licensing boundaries are documented explicitly in [GOVERNANCE.md](GOVERNANCE.md), [IP_POLICY.md](IP_POLICY.md), [CONTRIBUTING.md](CONTRIBUTING.md), [CLA.md](CLA.md), and [COPYRIGHT-ASSIGNMENT.md](COPYRIGHT-ASSIGNMENT.md).

EAIMS is not ISO, IEC, ANSI, a governmental body or an accredited certification scheme. See [DISCLAIMER.md](DISCLAIMER.md) and [TRADEMARK.md](TRADEMARK.md).

## Licensing and provenance

The detailed boundary is defined in [LICENSE](LICENSE): documentation, normative specification/assessment content and machine-readable specification data other than JSON Schemas are licensed under **CC BY 4.0**; code, tests, automation/build assets, Docker/Compose configuration, workflows and JSON Schemas are licensed under **Apache-2.0**. Public licenses do not transfer ownership, trademarks, governance authority or official-release authority.

See [PROVENANCE.md](PROVENANCE.md), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), [LICENSE-CODE.md](LICENSE-CODE.md), and [LICENSE-DOCS.md](LICENSE-DOCS.md).

## Migration and historical resources

The v0.2.1 research baseline remains part of repository history. See [MIGRATION-v0.2.1-to-v1.0.md](MIGRATION-v0.2.1-to-v1.0.md) and [research/EVOLUTION-0.2x-to-1.0.md](research/EVOLUTION-0.2x-to-1.0.md). Existing community, security, publication, RFC, decision and approved-implementation resources are intentionally retained during the v1 integration.

## Project website

**eaims.org**
