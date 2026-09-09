# EAIMS — Enterprise AI Maturity Standard

> An open, vendor-neutral, evidence-grounded, and executable specification for enterprise AI maturity, accountable autonomy, value realization, assurance, and operational risk.

**Candidate:** 1.0.0-fc16  
**Branch status:** v1.0.0-rc.1 preparation — not yet a stable release  
**Documentation and assessment content:** CC BY 4.0  
**Code, workflows, and JSON Schemas:** Apache-2.0

## EAIMS 1.0 candidate

EAIMS 1.0 moves from a primarily assessment-oriented maturity model toward an executable enterprise operating framework for AI value, autonomy, evidence, accountability, and risk.

The current candidate contains:

- **8 dimensions** and **30 capabilities**
- **5 maturity levels** with **150 capability-specific anchors**
- **206 structured requirements**, including **177 SHALL/SHALL_NOT** and **80 critical SHALL/SHALL_NOT** requirements
- explicit evidence classes, evidence confidence, validity states, counter-evidence, cutoff semantics, and assessment lineage concepts
- Human Accountability Boundary (HAB), Human Reserved decisions, autonomy levels A0–A5, and Agent Permission Envelope (APE)
- rule-based risk escalation and G0–G3 gate families
- capability-specific anchor eligibility, contextual applicability, and selected cross-capability dependencies
- Assessment Quality diagnostics and multi-assessor disagreement/resolution workflow
- three deterministic **synthetic** end-to-end reference implementations
- machine-readable specification, schemas, reference engine, tests, CLI, Docker/Compose configuration, and CI workflow

EAIMS supports predictive ML, generative AI, RAG, AI agents, third-party AI services, and cloud, hybrid, sovereign, or on-premises architectures. It does not prescribe a vendor, model, platform, or consulting provider.

## Core principle

> **AI maturity is not maximum automation. It is knowing where automation should stop, where human oversight is necessary, and where accountability must remain human.**

Autonomy should be earned through evidence, not assumed through capability, and should never outpace governance maturity.

## Project status and stewardship

EAIMS was founded and initially authored by **Elias Naserkhaki**, registrant and founding steward of **eaims.org**. Founder attribution records project origin and stewardship; it does not create accredited standards authority or override published governance.

EAIMS is not an ISO, IEC, ANSI, governmental, or accredited standard. It does not itself provide certification, legal compliance, regulatory conformity, or safety assurance. See [Disclaimer](DISCLAIMER.md), [IP Policy](IP_POLICY.md), [Origin](ORIGIN.md), and [Trademark Policy](TRADEMARK.md).

## Quick start — EAIMS 1.0 candidate

```bash
python -m pip install -e '.[test]'
eaims-validate
pytest -q
```

Validate and assess a synthetic reference fixture:

```bash
eaims validate-fixture reference-implementations/ri-01-api-consumed-analytics/input/fixture.yaml
eaims assess reference-implementations/ri-01-api-consumed-analytics/input/fixture.yaml --out run-output
```

Legacy v0.2.1 CLI commands remain available for backward compatibility:

```bash
eaims validate <v0.2.1-assessment.json>
eaims score <v0.2.1-assessment.json>
eaims report <v0.2.1-assessment.json> --format html --output report.html
```

## Canonical 1.0 candidate structure

| Need | Resource |
|---|---|
| Core specification | [`spec/core.yaml`](spec/core.yaml) |
| Capabilities and maturity anchors | [`spec/capabilities.yaml`](spec/capabilities.yaml) |
| Normative requirements | [`spec/requirements.yaml`](spec/requirements.yaml) |
| Anchor eligibility | [`spec/anchor-eligibility.yaml`](spec/anchor-eligibility.yaml) |
| Evidence model | [`spec/evidence.yaml`](spec/evidence.yaml) |
| Risk and gates | [`spec/risk.yaml`](spec/risk.yaml), [`spec/gates.yaml`](spec/gates.yaml) |
| Assessment semantics | [`spec/assessment.yaml`](spec/assessment.yaml) |
| Assessor protocol | [`spec/assessor-protocol.yaml`](spec/assessor-protocol.yaml) |
| Assessment Quality | [`spec/assessment-quality.yaml`](spec/assessment-quality.yaml) |
| Multi-assessor workflow | [`spec/multi-assessor.yaml`](spec/multi-assessor.yaml) |
| Executable engine | [`src/eaims/`](src/eaims/) |
| Synthetic reference cases | [`reference-implementations/`](reference-implementations/) |
| Independent-review package | [`review/`](review/) |
| Validation artifacts | [`validation/`](validation/) |
| v0.2.1 → 1.0 migration | [`docs/release/MIGRATION-v0.2.1-to-v1.0.md`](docs/release/MIGRATION-v0.2.1-to-v1.0.md) |

The v0.2.1 materials remain in repository history and selected legacy paths for compatibility and research reproducibility. The `spec/` directory is the canonical structured source for the 1.0 candidate.

## Validation status

The FC16 candidate has passed the local deterministic test and packaging suite, including canonical-integrity, installed-wheel, fixture, and reference-assessment checks. Hosted GitHub Actions, Docker/Compose runtime evidence, dependency/SBOM evidence, and independent external review are release gates and are not claimed complete until their corresponding branch runs or review records exist.

EAIMS 1.0 is **field-informed rather than field-validated**. Its design incorporates feasibility assessment, synthetic reference implementations, and enterprise pilot-readiness inputs. Formal multi-organization empirical validation and inter-rater reliability research remain part of the research agenda.

## Independent review

The [`review/`](review/) package provides adversarial review questions, structured feedback and resolution schemas, severity levels, and deterministic RC exit semantics. Reviewer identities are not required in public release artifacts; review records can use non-personal identifiers.

## Attribution policy

Public 1.0 release materials identify **Elias Naserkhaki** as the only named individual. Reviewers, assessors, enterprise design inputs, and synthetic actors use non-personal identifiers unless a future explicit publication decision changes that policy. See [`ATTRIBUTION-POLICY.md`](ATTRIBUTION-POLICY.md).

## Contributing and governance

Contributions require DCO sign-off and rights disclosure. See [Contributing](CONTRIBUTING.md), [Governance](GOVERNANCE.md), [Reviewer Program](REVIEWERS.md), [Sponsorship Policy](SPONSORSHIP.md), and [Financial Transparency](FINANCIAL_TRANSPARENCY.md). Funding cannot buy changes, favorable scores, certification, endorsement, or governance control.

## Publications

Books and research outputs: [EAIMS Publications](publications/README.md)

## Project website

https://eaims.org
