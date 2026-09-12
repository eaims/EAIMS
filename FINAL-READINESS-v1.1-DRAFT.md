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

## Validation required before normative candidate

- [ ] Latest full CI run passes
- [ ] At least two independent assessor passes over inter-rater cases
- [ ] Ambiguous cases resolved or explicitly retained as MV3/MV4 judgment
- [ ] Merge-candidate decision finalized for ADV-004, ADV-006, ADV-009
- [ ] Gate-effect thresholds reviewed against at least one critical (I4) scenario
- [ ] Candidate machine-verification paths implemented only after schema/runtime design is approved
- [ ] Backward-compatibility regression executed against all 1.0 reference outputs
- [ ] Review findings resolved with retained resolution history
- [ ] Legal/IP review confirms references remain conceptual and non-infringing
- [ ] Final normative spec/version identifiers assigned only at freeze

## Freeze blockers

Any of the following blocks normative freeze:

- unresolved collision with stable 1.0 requirement semantics;
- requirement without defensible applicability semantics;
- critical gate with undefined consequence;
- machine-verifiable claim that depends materially on human judgment;
- inability to preserve/reproduce 1.0.x historical assessment semantics;
- unresolved inter-rater ambiguity on critical requirements;
- evidence requirements that cannot be realistically collected without exposing protected operational secrets;
- external-framework language copied beyond permissible/reference use.

## Release decision

Current status: **DEVELOPMENT DRAFT — NOT READY FOR NORMATIVE FREEZE**

The package is structurally mature enough for review and validation, but not yet for release as EAIMS 1.1.
