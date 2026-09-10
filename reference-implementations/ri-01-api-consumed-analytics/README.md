# RI-01 — API-Consumed Analytics Assistant

Synthetic, operationally realistic reference implementation for EAIMS 1.0 Freeze Candidate 3.

It exercises model sourcing, floating provider dependencies, evaluation retention, structured-context applicability, partial-scope reporting, evidence provenance, gate semantics, and external-change-exposure consistency checks.

This is **not** a production deployment, customer pilot, empirical validation study, or evidence of third-party adoption.

## Run

```bash
PYTHONPATH=. python -m src.eaims.cli assess \
  reference-implementations/ri-01-api-consumed-analytics/input/fixture.yaml \
  --out reference-implementations/ri-01-api-consumed-analytics/runs/latest
```

Expected behavior includes a material risk band, a sourcing maturity constraint caused by missing provider-change re-evaluation, explicit G1 breaches/incomplete gates, and a material consistency finding for high external change exposure without provider-change re-evaluation.
