# EAIMS Paper 01 - Reproducibility Package

This directory supports the first research paper based on EAIMS.

## Scope

The analysis uses the three fictional assessment fixtures distributed with EAIMS:

- `examples/fictional-manufacturer.assessment.json`
- `examples/fictional-bank.assessment.json`
- `examples/fictional-cloud-company.assessment.json`

The fixtures are demonstration data only. They are not empirical organizational observations.

## Reproduce

From the repository root:

```bash
python -m unittest discover -s tests -v
python research/paper-01/sensitivity_analysis.py
```

The sensitivity script writes:

`research/paper-01/sensitivity_results.csv`

## Interpretation

The reference EAIMS v0.2 engine uses equal weighting and a fixed critical gate threshold of 2.0.

Alternative weights, gate thresholds, confidence thresholds, and critical-set memberships in this directory are external computational sensitivity simulations. They are research experiments and are not normative EAIMS v0.2 scoring rules.

The analysis evaluates computational behavior and classification stability. It does not establish construct validity, predictive validity, inter-rater reliability, or multi-organization generalizability.

## Research baseline

- EAIMS release: `v0.2.1`
- Git commit SHA: `6d1dbf1`
- Book DOI: `10.5281/zenodo.21853733`

The manuscript is currently under peer review. A research-artifact DOI should be added here only after a versioned archive DOI has actually been minted.

Do not cite `main` as the reproducibility baseline.
