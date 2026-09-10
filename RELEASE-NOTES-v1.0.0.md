# EAIMS 1.0.0 — Final Release Notes

EAIMS 1.0.0 marks the transition from AI maturity assessment to accountable AI operations.

## Canonical model

- 8 dimensions
- 30 capabilities
- 5 maturity levels
- 150 capability-specific anchors
- 206 normative and cross-cutting requirements
- 177 SHALL/SHALL_NOT requirements
- 80 critical SHALL/SHALL_NOT requirements

## Key additions

- Human Accountability Boundaries (HAB) and Human Reserved decisions
- A0–A5 AI autonomy classification
- Agent Permission Envelopes and delegated-authority constraints
- Operational Suspension Capability
- Model/System Sourcing Profiles and External Change Exposure
- Maturity Debt, Autonomy Debt, Assurance Gap, Risk Drift, Autonomy Drift and Scope Drift diagnostics
- evidence confidence, validity, event invalidation, counter-evidence and conflict semantics
- G0–G3 gate families and rule-based escalation
- capability-specific maturity-anchor eligibility
- Assessment Quality and multi-assessor disagreement/resolution protocols
- federated maturity and Pilot-to-Scale governance
- machine-readable specification, schemas and machine-verification rules

## Executable release validation

The release line was promoted after successful hosted validation on RC1 and successful re-validation after merge to `main`. The release gate includes:

- 186 executable tests
- canonical specification integrity validation
- CLI and synthetic reference-implementation smoke tests
- Python wheel build and standalone installed-wheel validation
- dependency vulnerability audit
- CycloneDX SBOM generation
- Docker image build and runtime validation
- Docker Compose configuration and runtime validation
- execution of all three synthetic reference implementations
- runtime evidence artifact capture

## Compatibility

The public Python modules `eaims.scoring` and `eaims.reporting` and the established `validate`, `score`, and `report` CLI paths remain available. EAIMS 1.0 adds the structured `validate-fixture`, `assess`, and `review` workflows.

## Evidence boundary

EAIMS 1.0 is **field-informed rather than field-validated**. It does not claim independent multi-organization empirical validation, accredited certification, regulatory approval, representative benchmarking, empirical inter-rater reliability, or completed external independent review. Formal validation remains part of the research agenda.

## Version provenance

The public release is `1.0.0`. The frozen normative source intentionally retains the internal provenance identifier `1.0.0-fc16` so the exact specification content validated through RC1 remains traceable. Promotion to final release does not imply a substantive normative rewrite after RC1.

## Licensing and stewardship

Documentation and normative specification content are licensed under CC BY 4.0; code, tests, workflows, Docker/Compose configuration and JSON Schemas are licensed under Apache-2.0, subject to the repository's detailed licensing and provenance files.

Author and founding steward: **Elias Naserkhaki**

Release theme: **EAIMS 1.0 — From AI Maturity Assessment to Accountable AI Operations**
