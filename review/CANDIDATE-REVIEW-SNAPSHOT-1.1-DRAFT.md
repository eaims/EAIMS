# EAIMS 1.1 Candidate-Freeze Review Snapshot

This file pins the exact technical review baseline for independent assessor calibration.

## Review baseline

- Pull request: #9
- Branch: `eaims-1.1-adversarial-agentic-governance`
- Review head: `9f7e4bc9f2658d72ba73ee3b7d05957c89af8609`
- Full validation run: EAIMS Validation #265
- CI status: PASS
- Candidate status: non-normative
- Review state: candidate-freeze review ready

## Superseded baseline

The earlier review baseline `fb21bc6f65647bd7f15caca61229fd5da48f5246` / CI #248 is superseded.

Reason: pre-review consistency hardening aligned the assessor protocol, migration guide, crosswalk, consolidation record, reviewer questions, and IR-05 with the final candidate decision that ADV-009 is development-history only and dependency concentration is assessed through strengthened MSP-005/MSP-008 semantics.

No assessor response tied to the superseded baseline should be mixed with responses tied to the current baseline.

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
