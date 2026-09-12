# EAIMS 1.1.0 — Adversarial & Agentic Governance

Released: 2026-09-12

EAIMS 1.1.0 extends the stable 1.0.x baseline with a normative adversarial and agentic governance overlay for material AI systems.

## Normative additions

EAIMS 1.1.0 adds nine new adversarial/agentic requirements:

- ADV-001 Adversarial Exposure Analysis
- ADV-002 Blast Radius Assessment
- ADV-003 Agent Credential Boundary
- ADV-004 Agent Privilege Attribution
- ADV-005 Adversarial Evaluation Coverage
- ADV-006 Runtime Abuse Evidence
- ADV-007 Adversarial Incident Containment
- ADV-008 AI Threat Intelligence Disposition
- ADV-010 Synthetic Identity and Representation Control

It also strengthens:

- MSP-005 — fallback/exit plus material provider-concentration exposure;
- MSP-008 — composite dependency trace plus concentration/single-point exposure.

ADV-009 remains a development-history identifier only and is not part of the normative 1.1 requirement set.

## Gate extensions

The G3 Autonomous / Agentic family is extended with G3-13 through G3-17 for blast radius, bounded privileged credentials, adversarial evaluation, runtime abuse evidence, and incident containment.

## Compatibility

- EAIMS 1.0.x assessments remain valid as 1.0.x results.
- Existing 1.0 capability and requirement identifiers are preserved.
- EAIMS 1.1.0 does not retroactively regrade historical assessments.
- The executable 1.0 reference outputs for RI-01, RI-02, and RI-03 remain reproducible.
- The 1.1 normative overlay is additive to the frozen 1.0.x base specification.

## Validation performed

Before release, the repository passed:

- full automated specification and repository validation;
- executable tests and CLI/package smoke tests;
- backward-compatibility regression against frozen 1.0 reference outputs;
- dependency audit and SBOM generation;
- Docker build and runtime validation;
- candidate, release-readiness, and reference/IP hygiene audits;
- worked applicability, critical I4, and inter-rater calibration cases.

## Validation limitation

This release is **maintainer-frozen**. It does not claim independent third-party assessor validation, accreditation, certification, regulatory approval, or endorsement by referenced organizations.

Independent assessor calibration remains encouraged as post-release validation. Findings may be addressed in later patch or minor releases without changing the historical status of 1.1.0.

## External references

NIST, OWASP, MITRE ATLAS, Anthropic threat-intelligence publications, and Google Threat Intelligence Group publications are used as conceptual or empirical references. EAIMS does not reproduce those frameworks or imply endorsement or formal equivalence.
