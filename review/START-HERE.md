# EAIMS 1.0 RC Review Package — Start Here

Thank you for reviewing EAIMS 1.0. This package is designed so that a reviewer can challenge the framework without first reconstructing the repository architecture.

## What this review is — and is not

This is an **independent release-candidate design review**. The objective is to identify conceptual defects, contradictions, missing controls, weak maturity anchors, evidence/scoring problems, enterprise applicability issues, and executable-specification failures before `v1.0.0-rc.1`.

It is **not** a request to certify EAIMS, endorse it, or treat the synthetic reference implementations as real deployments. EAIMS 1.0 has not yet established cross-sector empirical validity, inter-rater reliability, predictive validity, regulatory conformity, or production-deployment validation.

## Recommended review path (60–120 minutes)

1. Read `review/EXECUTIVE-BRIEF.md`.
2. Read `research/EVOLUTION-0.2x-to-1.0.md` for the redesign rationale.
3. Inspect `spec/capabilities.yaml`, `spec/anchor-eligibility.yaml`, `spec/requirements.yaml`, `spec/gates.yaml`, and `spec/evidence.yaml` for the areas relevant to your expertise.
4. Inspect one or more synthetic reference implementations under `reference-implementations/`.
5. Run the local validation commands if you are reviewing executability.
6. Complete `review/FEEDBACK-TEMPLATE.yaml` or `review/FEEDBACK-TEMPLATE.md`.

## Local executable checks

```bash
python -m pip install -e .
eaims-validate
pytest -q
```

Reference example:

```bash
eaims assess \
  reference-implementations/ri-03-high-impact-decision-support/input/fixture.yaml \
  --out run-output
```

Docker runtime evidence should be evaluated only in an environment with a working Docker daemon. The build environment used to assemble this review package did not provide one.

## What we most want reviewers to attack

Please prioritize structural weaknesses over wording. Useful findings include contradictory requirements, maturity levels that cannot be observed reliably, controls that are unrealistic at enterprise scale, hidden assumptions, evidence rules that can be gamed, unsafe autonomy/HAB semantics, invalid aggregation behavior, or cases where the executable implementation disagrees with the written specification.

A review that concludes “not ready” is useful if it identifies traceable reasons.
