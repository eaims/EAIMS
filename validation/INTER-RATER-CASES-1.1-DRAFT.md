# EAIMS 1.1 Draft — Inter-Rater Worked Cases

> These cases are designed to expose ambiguous assessor interpretation before normative freeze.

## Case IR-01 — Shared service account with scoped API token

A material A4 service agent executes under a shared technical service account. The API token is scoped to refund operations, capped at 100 units, revocable independently, and all actions contain a unique agent execution ID plus approving workflow ID.

### Expected interpretation

- ADV-003: **SATISFIED or PARTIALLY_SATISFIED**, depending on whether organizational policy requires unique workload identities.
- ADV-004: **SATISFIED** if privileged actions can be attributed to the actual agent execution and approving authority.
- Key distinction: shared account name alone is not decisive; bounded authorization and traceable execution context are the material facts.

### Calibration note

Assessors should not automatically fail ADV-003 merely because a shared service account exists if authorization is scoped, revocable and independently attributable.

## Case IR-02 — Kill switch stops process but token remains active

A material agent can be stopped within seconds. However, its external API credential remains valid for 24 hours and could still be used by a compromised worker or residual process.

### Expected interpretation

- Existing suspension control may be operational.
- ADV-007: **NOT_SATISFIED**.
- G3-17: **BREACH**.
- Reason: process termination is not equivalent to containment of authority.

## Case IR-03 — Threat report reviewed, no action required

The security team reviews a major provider threat report, maps all reported techniques to the AI inventory, finds no applicable exposure, documents rationale, and records reviewer/approval.

### Expected interpretation

- ADV-008: **SATISFIED**.
- No control change is required because disposition can validly be NOT_APPLICABLE.
- Reading a report alone would not be sufficient; documented exposure mapping and disposition are required.

## Case IR-04 — Functional red-team only

An agent passes extensive functional tests and safety policy tests but has never been tested for prompt injection, malicious tool output, credential misuse, unsafe delegation, or exfiltration scenarios despite credible exposure.

### Expected interpretation

- ADV-005: **NOT_SATISFIED**.
- G3-15: **BREACH**.
- Functional coverage does not substitute for adversarial coverage.

## Case IR-05 — Single provider with strong exit plan

A business-critical AI service depends on one external model provider, but prompts/configuration are portable, an alternate provider is validated quarterly, data export is available, and failover is tested.

### Expected interpretation

- ADV-009: **SATISFIED**.
- Single-provider dependency does not itself imply failure; concentration risk must be analyzed and managed.

## Case IR-06 — Synthetic spokesperson disclosed as AI

A public AI spokesperson uses a persistent persona, clearly discloses that it is AI-generated, has formal brand authorization, rate limits, audit logs, and escalation rules.

### Expected interpretation

- ADV-010: **APPLICABLE and SATISFIED**.
- Synthetic identity is not inherently prohibited; maturity depends on governance, authorization, provenance/disclosure where appropriate, and monitoring.

## Case IR-07 — Missing applicability evidence

An assessor cannot determine whether a decision-support system can execute external actions because architecture documentation is incomplete.

### Expected interpretation

- Relevant action-dependent requirements: **CONDITIONALLY_APPLICABLE** or result **INSUFFICIENT_EVIDENCE**.
- They must not be marked NOT_APPLICABLE solely because evidence is absent.

## Calibration objective

Two independent assessors should reach the same requirement state and gate consequence for each case. Any case with persistent disagreement indicates one of:

- activation rule ambiguity;
- requirement wording ambiguity;
- evidence-threshold ambiguity;
- gate-effect ambiguity.

Such ambiguity must be resolved before normative freeze.
