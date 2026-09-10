# EAIMS 1.0 FC16 — Critical Requirement Verification Audit

FC16 distinguishes **machine-executable verification**, **scenario/reference executable evidence**, and **human/hybrid assessor protocol coverage**. These are not interchangeable.

## Strict results

- Critical SHALL/SHALL_NOT requirements: **80**
- Critical MV1/MV2 requirements: **33**
- MV1/MV2 with explicit executable verification rules: **33/33 (100%)**
- Critical MV3/MV4 requirements: **47**
- MV3/MV4 with explicit assessor protocol: **47/47 (100%)**
- Critical requirements with at least one executable test mapping (machine rule or existing scenario/reference test): **40/80 (50.0%)**
- Critical requirements with an explicit verification disposition (machine rule or assessor protocol): **80/80 (100%)**

**Important:** 100% disposition coverage is not 100% machine automation. Forty-seven critical MV3/MV4 requirements intentionally retain human or hybrid judgment.

## Coverage by machine-verifiability class

- **MV1:** 2 total — 2 with executable mapping; 0 with assessor protocol
- **MV2:** 31 total — 31 with executable mapping; 0 with assessor protocol
- **MV3:** 43 total — 7 with executable mapping; 43 with assessor protocol
- **MV4:** 4 total — 0 with executable mapping; 4 with assessor protocol

## RC interpretation

- FC16 closes the previous gap for critical MV1/MV2 requirements by giving every one an explicit, executable positive and negative verification path.
- FC16 gives every critical MV3/MV4 requirement a standardized assessor record, evidence expectation, rationale requirement, and decision semantics.
- Existing HAB, recourse, autonomy, evidence-conflict and reference-implementation tests provide executable coverage for selected MV3 requirements in addition to their assessor protocols.
- This does **not** establish empirical validity, inter-rater reliability, or production certification readiness.

## Remaining RC blockers

- Run Dockerfile and both Compose configurations in a real Docker runtime and retain run evidence.
- Execute an external/independent RC review and resolve P0/P1 findings.
- Complete capability-specific executable anchor eligibility beyond the generic E1–E4 floor.
- Calibrate provisional coverage/band/operating-cycle thresholds through reference and field evaluation.
- Add assessor-protocol worked examples beyond the single conformance example and exercise multi-assessor disagreement handling.
