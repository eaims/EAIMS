# EAIMS 1.1 Draft — Requirement Consolidation Decision Record

> Historical development decision record for RFC 0004. **Superseded for candidate-freeze decisions by `docs/FINAL-CONSOLIDATION-DECISION-1.1-DRAFT.md`.**

## Final candidate disposition

| Candidate | Final candidate decision | Rationale |
|---|---|---|
| ADV-001 | KEEP | Adversarial exposure is not explicitly required by existing generic risk analysis. |
| ADV-002 | KEEP | Blast radius is distinct from permission boundaries and reversibility. |
| ADV-003 | KEEP | Agent identity does not equal bounded credential/authorization scope. |
| ADV-004 | KEEP | Privileged action attribution to both workload identity and initiating/approving authority remains distinct. |
| ADV-005 | KEEP | Existing evaluation requirements do not explicitly mandate adversarial scenario coverage. |
| ADV-006 | KEEP | Investigation-grade runtime abuse evidence remains a distinct operational assurance property. |
| ADV-007 | KEEP | Existing incident/suspension controls do not explicitly require authority/credential/tool/memory containment. |
| ADV-008 | KEEP | No existing closed-loop AI-specific threat-intelligence disposition requirement. |
| ADV-009 | MERGED INTO MSP-005 / MSP-008 | Concentration risk remains material but belongs in sourcing/dependency semantics. |
| ADV-010 | KEEP, CONDITIONAL | Synthetic identity/representation exposure is materially distinct and context-dependent. |

## Historical development path

Earlier development work considered ADV-004, ADV-006, and ADV-009 as merge candidates. Worked-case review and gate analysis led to the final draft consolidation decision:

- ADV-004: retained;
- ADV-006: retained;
- ADV-009: consolidated into strengthened MSP-005/MSP-008 semantics.

The development identifier ADV-009 remains visible only for traceability. It must not be scored separately in candidate-freeze assessment.

## Candidate delta

The candidate therefore consists of:

- **9 new ADV requirements**; and
- **2 strengthened existing MSP requirements**: MSP-005 and MSP-008.

## Freeze criterion

Any future consolidation change before normative freeze must show that:

1. assessment outcomes remain explainable;
2. no gate loses a distinct control consequence;
3. evidence expectations remain explicit;
4. inter-rater interpretation does not degrade;
5. migration semantics remain reproducible.

For the current candidate-freeze review, the final disposition above is authoritative.
