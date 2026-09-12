# EAIMS 1.1 Candidate-Freezer Review Snapshot

This file pins the exact technical review baseline for independent assessor calibration.

## Review baseline

- Pull request: #9
- Branch: `eaims-1.1-adversarial-agentic-governance`
- Review head: `fb21bc6f65647bd7f15caca61229fd5da48f5246`
- Full validation run: EAIMS Validation #248
- CI status: PASS
- Candidate status: non-normative
- Review state: candidate-freeze review ready

## Assessor rule

Independent assessors should evaluate only this pinned review baseline unless a later snapshot explicitly supersedes it.

If the branch advances after this snapshot:

- existing assessor responses remain tied to this SHA;
- responses from different SHAs must not be compared as if they reviewed the same candidate;
- any material semantic change requires a new review snapshot and, where relevant, re-assessment.

## Review artifacts

Assessors should use:

- `validation/INTER-RATER-CASES-1.1-DRAFT.md`
- `review/INDEPENDENT-ASSESSOR-CALIBRATION-1.1-DRAFT.md`
- `review/assessor-response-template-1.1-draft.yaml`
- `spec/adversarial-agentic-normative-candidate-1.1.yaml`
- `spec/adversarial-agentic-candidate-projection-1.1.yaml`
- `docs/ASSESSOR-PROTOCOL-ADVERSARIAL-1.1-DRAFT.md`

## Comparison

After two genuinely independent responses are complete, compare them with:

`python tools/compare_v11_assessors.py assessor-a.yaml assessor-b.yaml --json`

Critical disagreements remain freeze blockers until dispositioned.
