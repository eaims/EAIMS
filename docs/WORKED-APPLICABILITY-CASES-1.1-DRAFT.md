# EAIMS 1.1 Draft — Worked Applicability Cases

> Non-normative assessor training material for RFC 0004.

## Case A — API-consumed analytics assistant

**Context:** Material internal analytics assistant; non-agentic; advisory autonomy (A1); external API model provider; no public synthetic persona or external action.

Expected activation:

| Requirement | Expected | Reason |
|---|---|---|
| ADV-001 | APPLICABLE | Material AI still has adversarial exposure such as prompt/context manipulation and provider risk |
| ADV-002 | NOT_APPLICABLE | No action-taking or A2+ autonomy |
| ADV-003 | NOT_APPLICABLE | No privileged agent authority |
| ADV-004 | NOT_APPLICABLE | No privileged agent action |
| ADV-005 | CONDITIONALLY_APPLICABLE | Assessor must establish credible adversarial exposure for the actual use context |
| ADV-006 | NOT_APPLICABLE | No action-taking behavior |
| ADV-007 | NOT_APPLICABLE | Non-agentic, low autonomy |
| ADV-008 | APPLICABLE | Organization operates material AI |
| ADV-009 | APPLICABLE | External provider dependency exists |
| ADV-010 | NOT_APPLICABLE | No synthetic identity/representation exposure |

**Assessor caution:** External dependency does not automatically imply high concentration risk; it only activates the requirement.

## Case B — Enterprise autonomous service agent

**Context:** Material agent; A4 observed autonomy; customer account data; external communication; refund API; material transaction authority.

Expected activation:

| Requirement | Expected | Reason |
|---|---|---|
| ADV-001 | APPLICABLE | Material adversarial exposure |
| ADV-002 | APPLICABLE | Agentic and A4 |
| ADV-003 | APPLICABLE | External actions and material transaction authority |
| ADV-004 | APPLICABLE | Privileged/transactional actions require attribution |
| ADV-005 | APPLICABLE | Tool misuse, prompt injection, authority abuse and exfiltration are credible |
| ADV-006 | APPLICABLE | The system performs actions |
| ADV-007 | APPLICABLE | Agentic/A4 |
| ADV-008 | APPLICABLE | Organization operates material AI |
| ADV-009 | APPLICABLE | External model/provider dependency |
| ADV-010 | NOT_APPLICABLE | Customer communication alone does not create synthetic-persona exposure absent impersonation/representation behavior |

**Assessor caution:** This case already contains an authority-limit breach in the EAIMS 1.0 fixture. A 1.1 assessment must preserve that counter-evidence; new controls cannot overwrite it.

## Case C — High-impact employment decision support

**Context:** Material, non-agentic decision-support system; A2; high-impact employment context; final adverse decision reserved to humans.

Expected activation:

| Requirement | Expected | Reason |
|---|---|---|
| ADV-001 | APPLICABLE | High-impact AI has credible adversarial and misuse exposure |
| ADV-002 | APPLICABLE | A2 means execution/action may occur with approval and blast radius matters |
| ADV-003 | NOT_APPLICABLE | No agentic privileged credential context established |
| ADV-004 | NOT_APPLICABLE | No privileged agent action established |
| ADV-005 | APPLICABLE | Adversarial manipulation of high-impact decisions is credible |
| ADV-006 | CONDITIONALLY_APPLICABLE | The fixture records AI execution of a reserved decision, but action-taking architecture must be confirmed |
| ADV-007 | NOT_APPLICABLE | Non-agentic and not A3+ |
| ADV-008 | APPLICABLE | Organization operates material AI |
| ADV-009 | CONDITIONALLY_APPLICABLE | Provider/dependency context is not sufficiently described in the fixture |
| ADV-010 | NOT_APPLICABLE | No synthetic identity or persuasive automation exposure |

**Assessor caution:** A human-reserved breach is not converted into an agentic classification merely because AI improperly executed a decision.

## Case D — Public synthetic spokesperson

**Context:** Material AI system generates persistent branded personas, publishes persuasive public content, and can schedule posts but cannot make financial or infrastructure changes.

Expected activation:

- ADV-001: APPLICABLE
- ADV-002: APPLICABLE
- ADV-003: APPLICABLE if posting credentials permit external publication
- ADV-004: APPLICABLE if publication is treated as a privileged organizational action
- ADV-005: APPLICABLE
- ADV-006: APPLICABLE
- ADV-007: APPLICABLE when autonomous scheduling/execution reaches A3+
- ADV-008: APPLICABLE
- ADV-009: APPLICABLE if externally dependent
- ADV-010: APPLICABLE

Required evidence should include representation authorization, provenance/disclosure rules where appropriate, publication logs, audience/amplification controls, credential scope, and escalation routes.

## General assessor rule

Do not infer NOT_APPLICABLE from missing evidence. Missing context produces CONDITIONALLY_APPLICABLE or INSUFFICIENT_EVIDENCE until a defensible applicability rationale is established.
