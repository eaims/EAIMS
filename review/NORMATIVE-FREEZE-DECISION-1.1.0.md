# EAIMS 1.1.0 — Normative Freeze Decision

## Decision

**Status: MAINTAINER-FROZEN FOR RELEASE**

On 2026-09-12, the EAIMS maintainer approved normative freeze of the EAIMS 1.1 adversarial and agentic governance overlay as version **1.1.0**.

The decision follows successful technical validation, compatibility regression, candidate consolidation, reference/IP hygiene review, and release-readiness checks.

## Normative scope

The normative 1.1.0 overlay is:

`spec/adversarial-agentic-1.1.yaml`

It adds 9 ADV requirements, strengthens MSP-005 and MSP-008, and extends G3 with G3-13 through G3-17.

## Maintainer decision on independent review

Independent assessor calibration is **not a release prerequisite for 1.1.0**.

Instead:

- 1.1.0 is released as a maintainer-frozen normative version;
- no claim of independent third-party validation is made;
- no claim of accreditation, certification, external endorsement, or regulatory approval is made;
- independent assessor calibration remains a post-release validation activity;
- material findings may produce a later patch/minor revision with retained history.

This avoids misrepresenting unperformed external review while allowing the completed normative work to be published.

## Compatibility

- EAIMS 1.0.x remains historically valid.
- Historical 1.0.x results are not regraded.
- Frozen 1.0 canonical files remain preserved.
- The 1.1 overlay is version-scoped and additive.

## Release authorization

The maintainer authorizes:

- normative status for the 1.1 overlay;
- version identifier 1.1.0;
- merge to main after CI passes;
- release publication through the repository release workflow.

No external validation claim is authorized.
