# EAIMS 1.1 Candidate — Release-Readiness Audit Criteria

> Pre-freeze review artifact. This document does not approve release.

## Audit domains

### 1. Versioning and status
- All 1.1 candidate artifacts remain explicitly non-normative.
- EAIMS 1.0.x canonical spec files retain their 1.0 identifiers until explicit freeze.
- Draft/candidate labels are not represented as released normative status.

### 2. Requirement integrity
- No new ID collides with EAIMS 1.0.
- No orphan capability reference exists.
- ADV-009 is not present as a final candidate requirement.
- MSP-005 and MSP-008 remain the only amended 1.0 requirement IDs in this package.

### 3. Gate integrity
- G3-13 through G3-17 do not collide with existing G3 gate IDs.
- Every gate references valid active candidate requirements.
- Gate consequences remain explicit and non-numeric.

### 4. Candidate/development separation
- Development artifacts may retain ADV-009 for traceability.
- Candidate assessment semantics must use strengthened MSP-005/MSP-008 instead.
- Development-only IDs must not leak into candidate projection or gate semantics.

### 5. Backward compatibility
- Historical 1.0.x assessments remain valid as 1.0.x results.
- Candidate 1.1 semantics do not retroactively regrade them.
- Migration requires explicit reassessment of newly applicable or strengthened requirements.

### 6. Reference and IP hygiene
- External frameworks are referenced conceptually and not copied.
- EAIMS does not claim endorsement, equivalence, certification, or clause-level compliance unless independently established.
- Public references remain clearly attributable.

### 7. Package completeness
- Every artifact listed in the package manifest exists.
- No duplicate manifest paths.
- Tests and audit tools are included in the package.

## Freeze blockers

Candidate freeze is blocked by any of:

- failing CI;
- failing release-readiness audit;
- orphan or colliding IDs;
- unresolved candidate/development semantic conflict;
- ambiguous critical gate consequence;
- inability to preserve 1.0.x historical semantics;
- unresolved critical inter-rater ambiguity;
- external-framework language that creates IP/equivalence risk;
- candidate artifact incorrectly marked normative before explicit freeze.
