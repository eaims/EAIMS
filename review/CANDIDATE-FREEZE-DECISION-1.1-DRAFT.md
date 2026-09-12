# EAIMS 1.1 — Candidate Freeze Decision Record

> This record governs transition from development draft to candidate-freeze review. It is not a release approval.

## Current decision

**Status: HOLD FOR CANDIDATE-FREEZE REVIEW**

The technical package is sufficiently mature for candidate-freeze review when all automated checks are green. Normative freeze remains blocked by unresolved human-review requirements.

## Technical readiness

- Candidate normative overlay defined.
- Candidate projection defined.
- ADV-004 and ADV-006 retained as distinct candidate requirements.
- ADV-009 consolidated into strengthened MSP-005 / MSP-008 semantics.
- G3-13 through G3-17 defined with explicit consequences.
- Activation/applicability semantics defined.
- Evidence expectations defined.
- Critical I4 worked case defined.
- Development and candidate semantics separated.
- Candidate package manifest defined.
- Candidate structural audit implemented.
- Release-readiness audit implemented.
- Reference/IP repository-hygiene audit implemented.
- Executable regression test recomputes RI-01, RI-02, and RI-03 and compares semantic output plus deterministic result_hash against frozen 1.0 expected outputs.
- Review findings log and resolution-retention policy defined.

## Human-review blockers

The following shall not be represented as completed until independently performed:

1. At least two independent assessor passes over the inter-rater cases.
2. Resolution of any critical semantic disagreements discovered by those assessors.
3. Independent legal/IP review if deemed necessary for normative publication.

## Freeze transition criteria

Candidate-freeze review may begin when:

- full CI passes;
- candidate audit passes;
- release-readiness audit passes;
- reference/IP hygiene audit passes;
- executable 1.0 regression passes;
- no critical review finding is OPEN.

Normative freeze may occur only after the independent-assessor requirement and any required independent legal/IP review are completed.

## Release protection

A green CI result alone does not authorize:

- changing `normative: false` to true;
- changing stable 1.0 canonical files;
- assigning final 1.1 release identifiers;
- merging a normative 1.1 release into main;
- claiming external certification, endorsement, or equivalence.

Any such transition requires an explicit freeze decision and retained decision history.
