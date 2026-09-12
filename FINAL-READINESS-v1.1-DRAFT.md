# EAIMS 1.1 Adversarial & Agentic Governance — Draft Readiness Checklist

> Development readiness checklist for RFC 0004. This is not a release approval.

## Design completeness

- [x] Problem statement and evidence basis documented
- [x] Candidate requirements defined
- [x] Existing EAIMS 1.0 overlap analyzed
- [x] Candidate gate extensions defined
- [x] Gate consequences defined
- [x] Applicability/activation semantics defined
- [x] Anchor-eligibility overlay defined
- [x] Evidence expectations defined
- [x] Candidate machine-verification rules limited to defensible cases
- [x] Migration approach documented
- [x] External conceptual crosswalk documented
- [x] Assessor protocol documented
- [x] Threat-intelligence operating protocol documented
- [x] Positive/negative fixtures added
- [x] Existing reference implementations mapped for regression
- [x] Inter-rater ambiguity cases added
- [x] Requirement consolidation candidates documented
- [x] Merge-candidate decision finalized for ADV-004, ADV-006, ADV-009
- [x] Gate-effect thresholds reviewed against a critical I4 scenario
- [x] Candidate projection separates final semantics from development-only ADV-009
- [x] Candidate package manifest defined
- [x] Candidate pre-freeze audit implemented
- [x] Release-readiness audit implemented
- [x] Reference/IP repository-hygiene audit implemented
- [x] Independent assessor calibration worksheet and comparison policy defined
- [x] Assessor response template and automated comparison utility defined
- [x] IR-05 updated to final candidate MSP-005/MSP-008 semantics
- [x] Assessor protocol, migration guide, crosswalk, consolidation record, and reviewer questions aligned to final ADV-009 consolidation semantics
- [x] Executable 1.0 output-regression test added for RI-01, RI-02, and RI-03
- [x] Full CI #265 passed on final semantic review head 9f7e4bc9f2658d72ba73ee3b7d05957c89af8609
- [x] Executable backward-compatibility regression passed against frozen 1.0 reference outputs
- [x] Candidate package is technically ready for candidate-freeze review

## Validation required before normative freeze

- [ ] At least two independent assessor passes over inter-rater cases
- [ ] Ambiguous cases resolved or explicitly retained as MV3/MV4 judgment
- [ ] Candidate machine-verification paths implemented only after schema/runtime design is approved
- [ ] Review findings resolved with retained resolution history
- [ ] Independent legal/IP review completed if required for release
- [ ] Final normative spec/version identifiers assigned only at freeze

## Freeze blockers

Any of the following blocks normative freeze:

- unresolved collision with stable 1.0 requirement semantics;
- requirement without defensible applicability semantics;
- critical gate with undefined consequence;
- machine-verifiable claim that depends materially on human judgment;
- unresolved inter-rater ambiguity on critical requirements;
- evidence requirements that cannot be realistically collected without exposing protected operational secrets;
- external-framework language copied beyond permissible/reference use;
- open critical review finding;
- failing candidate, release-readiness, output-regression, or reference/IP hygiene audit.

## Release decision

Current status: **CANDIDATE-FREEZE REVIEW READY — NOT NORMATIVELY FROZEN**

The technical package and full CI/regression are green. Normative freeze remains blocked by genuinely independent assessor calibration, any resulting critical ambiguity resolution, retained review closure, and any independent legal/IP review required before publication.
