# Known Limitations at FC16 Review Stage

The following limitations are intentionally disclosed to reviewers and should not be interpreted as hidden defects:

- No completed multi-organization empirical validation study.
- No demonstrated inter-rater reliability from real independent assessors.
- Maturity-band thresholds, Assessment Quality thresholds, L4 operating-cycle defaults, and L5 adaptation-cycle defaults are design-calibrated rather than empirically calibrated.
- No predictive or criterion-validity claim linking EAIMS scores to business outcomes.
- No claim of ISO/IEC, regulatory, accreditation, or certification conformity.
- The three published reference implementations are synthetic and deterministic by design.
- Enterprise pilot-readiness inputs are anonymized design inputs, not production deployments.
- Automated evidence collection from real enterprise systems is not implemented as a production connector suite.
- Some requirements necessarily depend on structured human judgment (MV3/MV4).
- Docker/Compose runtime execution has not been demonstrated in the package assembly environment because no Docker daemon was available there; hosted CI includes the intended runtime steps.
- Federated-enterprise assessment is specified conceptually but has less executable reference coverage than the three primary system/use-case scenarios.
- Risk and gate escalation rules are scenario-tested but not cross-sector empirically calibrated.

A reviewer should still flag any limitation that makes the framework unsuitable for RC, or any limitation that is incorrectly described here.
