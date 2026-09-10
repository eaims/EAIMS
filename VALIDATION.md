# EAIMS 1.0.0 — Validation Status

## Demonstrated for the final release line

- 8 dimensions, 30 canonical capabilities and 150 capability-specific maturity anchors are machine-readable.
- The catalog contains 206 requirements, including 177 SHALL/SHALL_NOT and 80 classified critical.
- Canonical referential-integrity validation passes.
- Evidence, capability-specific maturity-anchor eligibility, risk/gate logic, selected HAB/APE logic, deterministic hashing and reporting are executable.
- All **33 critical MV1/MV2** requirements have explicit machine-verification rules with positive and negative executable tests.
- All **47 critical MV3/MV4** requirements have explicit assessor-protocol entries with required decision, rationale, evidence references and timestamp semantics.
- All 150 canonical anchor eligibility rules are machine-readable and interpreted by the executable engine.
- Three synthetic reference implementations execute end-to-end.
- Assessment Quality rules, multi-assessor disagreement classification, explicit resolution records and inter-rater-ready exports are executable through synthetic worked cases.
- Machine-derived G2/G3 findings take precedence over contradictory manual PASS assertions for modeled machine-checkable controls.
- Legacy public Python APIs `eaims.scoring` and `eaims.reporting` remain available.

## Hosted release validation

The RC1 source was validated on GitHub-hosted CI before promotion, and the merged `main` commit was validated again successfully.

The `main` validation run completed with all release-gate steps successful, including:

- repository/pre-push audit;
- canonical specification validation;
- **186 executable tests**;
- CLI and reference-implementation smoke tests;
- Python wheel build;
- standalone installed-wheel validation outside the source repository;
- dependency vulnerability audit;
- CycloneDX Python dependency SBOM generation;
- Docker image build;
- read-only Docker runtime validation;
- Docker Compose configuration validation;
- minimal Compose runtime validation;
- reference Compose runtime execution of all three synthetic reference implementations;
- runtime evidence capture and artifact upload.

The dependency audit reported no known vulnerabilities in auditable dependencies at the time of the hosted run. The local EAIMS package itself was not found on PyPI and therefore was not treated as a third-party dependency by that audit.

## Critical verification audit

EAIMS 1.0 distinguishes three coverage claims:

1. **Machine-rule coverage:** 33/33 critical MV1/MV2 requirements (100%).
2. **Assessor-protocol coverage:** 47/47 critical MV3/MV4 requirements (100%).
3. **Strict executable critical coverage:** machine rules plus existing direct scenario/reference mappings cover 40/80 critical requirements (50.0%).

The third number is intentionally lower because assessor-protocol coverage is not counted as machine execution.

## Selected executable behaviors

- installed Python CLI/package execution;
- Docker/Compose packaging and least-privilege runtime validation;
- assessment evidence after cutoff is rejected;
- invalidated evidence cannot support current higher maturity;
- capability-specific anchors combine requirement satisfaction, evidence class, counter-evidence and cycle rules;
- L4/L5 cycle and adaptation constraints are executable;
- higher-order observations are preserved when prerequisites block the award;
- explicit hard/supporting cross-capability dependencies are executable;
- missing evidence does not automatically force L1;
- critical failure constrains higher maturity;
- risk and gate-family escalation;
- Human Reserved decision contradictions and observed execution breaches;
- missing high-impact recourse;
- autonomy drift and permission-envelope violations;
- evidence conflict preservation;
- deterministic result hashes;
- all critical MV1/MV2 verification rules execute both pass and fail paths;
- assessor records reject missing rationale/evidence and unjustified N/A decisions.

## Evidence and research boundary

The following are **not** established by the current release evidence:

- independent multi-organization empirical validation;
- empirical inter-rater reliability;
- automated evidence collection from real enterprise systems;
- cross-sector threshold calibration;
- predictive, construct or criterion validity;
- regulatory conformity or accredited certification;
- representative industry benchmarking;
- external independent review completion.

EAIMS 1.0 is therefore described as **field-informed rather than field-validated**. Its design incorporates feasibility observations, realistic synthetic reference implementations and enterprise pilot-readiness inputs. Formal multi-organization validation remains part of the research agenda.

## Independent-review readiness

The repository contains a structured independent review protocol, reviewer brief, adversarial review questions, known-limitations disclosure, feedback template/schema, explicit review exit criteria, findings ledger and resolution semantics. This demonstrates **review-process readiness**, not completion of independent external review.

## Legal/IP/Governance validation

The reviewed Legal/IP/Governance controls are integrated in the repository. Executable legal/provenance consistency checks are part of the release validation path. Licensing boundaries distinguish CC BY 4.0 specification/documentation content from Apache-2.0 software and executable assets, while governance and contribution-rights documents separately address ownership, contribution acceptance, provenance and release authority.

These repository checks are not a substitute for jurisdiction-specific legal advice or a global title/plagiarism opinion.

## Version and provenance

The public release version is **1.0.0**. The frozen normative source retains the internal provenance identifier **`1.0.0-fc16`** so that generated evidence and the exact content validated during RC1 remain traceable. No substantive normative change is implied by promotion from the validated RC1 content to the final public version.
