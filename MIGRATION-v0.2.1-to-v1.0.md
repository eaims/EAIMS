# Migration Guide — EAIMS v0.2.1 Research Baseline to EAIMS 1.0

EAIMS 1.0 is a structural redesign, not a simple questionnaire revision.

## Canonical architecture change

| v0.2.1 research baseline | v1.0 freeze candidate |
|---|---|
| 9 dimensions | 8 dimensions |
| 27 capabilities | 30 capabilities |
| 6 maturity levels | 5 maturity levels |
| 162 observable anchors | 150 capability-specific anchors |
| maturity + evidence confidence | maturity + evidence confidence retained, with expanded evidence validity and eligibility semantics |

Existing v0.2.1 assessment results must **not** be relabeled as v1.0 results. Reassessment or an explicit migration study is required.

## Major semantic changes

- Human Accountability Boundary and Human Reserved decision semantics.
- A0–A5 autonomy governance and Agent Permission Envelope controls.
- Model/System Sourcing Profile and External Change Exposure.
- Explicit full / partial / targeted assessment semantics.
- `INDETERMINATE`, `NOT_APPLICABLE`, and `NOT_ASSESSED` are distinct.
- Capability-specific L1–L5 eligibility rules and preservation of higher-order evidence.
- Gate results are explicit (`PASS`, `BREACH`, `INCOMPLETE`, `NOT_APPLICABLE`) and cannot be hidden by averaging.
- Assessment Quality remains separate from organizational maturity.
- Multi-assessor disagreement is resolved explicitly rather than averaged.
- Evidence provenance, cutoff, invalidation, counter-evidence and conflict semantics are stronger.

## Data migration principle

Historical evidence may be reused only if it remains relevant, traceable and valid under v1 evidence rules. Historical scores themselves are not mechanically converted.

## API/schema migration

Treat v1 schemas as a new contract. Consumers should validate by `spec_version` / `schema_version` and reject silent reinterpretation of v0.2.x objects.
