# Critical Assessor Protocol — FC16

EAIMS deliberately does not pretend that all enterprise maturity requirements can be automated. Critical MV3/MV4 requirements retain hybrid or human judgment where context, authority, competence, organizational behavior or substantive effectiveness must be assessed.

## Required assessor record

Every critical MV3/MV4 decision must record at least:

- `requirement_id`
- `assessor_id`
- `decision`
- `rationale`
- `evidence_refs`
- `assessed_at`

Allowed decisions are:

- `SATISFIED`
- `NOT_SATISFIED`
- `INSUFFICIENT_EVIDENCE`
- `NOT_APPLICABLE`

`NOT_APPLICABLE` additionally requires an applicability rationale. Absence of evidence is not sufficient to claim N/A.

## Decision discipline

A SATISFIED result requires evidence and a written explanation of why the evidence demonstrates the requirement in the assessed context. A NOT_SATISFIED result means evidence or direct observation demonstrates a failure. INSUFFICIENT_EVIDENCE is used when the requirement is applicable but evidence is unavailable, weak or materially conflicted.

Assessor independence affects **Assessment Quality**, not the underlying maturity score directly.

## Coverage

- Critical MV3/MV4: **47**
- Explicit protocol entries: **47**
- Protocol coverage: **100%**

Selected MV3 requirements additionally have executable scenario/reference tests, but protocol coverage must not be described as machine automation.
