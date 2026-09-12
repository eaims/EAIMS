# Draft Migration Guide — EAIMS 1.0.x to 1.1

> **Development document.** EAIMS 1.0.x remains the stable baseline. This guide describes the candidate migration path if RFC 0004 is adopted.

## Migration principle

EAIMS 1.1 is designed as an additive evolution rather than a replacement of 1.0.x. Existing capability IDs remain stable and historical 1.0.x assessments are not retroactively regraded.

## What remains unchanged

- the core maturity scale L1–L5;
- the existing capability identifiers;
- evidence-before-maturity;
- confidence separation;
- critical-gate semantics;
- impact, autonomy, reversibility, scale, velocity, and detectability concepts;
- existing G0/G1/G2/G3 gate families unless explicitly extended.

## Candidate additions

| EAIMS 1.1 candidate | Existing home | What is new |
|---|---|---|
| EAIMS-ADV-001 Adversarial Exposure Analysis | GOV-02 | Explicit adversarial misuse/abuse/privilege/dependency exposure |
| EAIMS-ADV-002 Blast Radius Assessment | GOV-04 | Maximum credible scope of harmful/unauthorized agent action |
| EAIMS-ADV-003 Agent Credential Boundary | TEC-04 | Scoped/revocable authorization for privileged agents |
| EAIMS-ADV-004 Agent Privilege Attribution | TEC-04 | Attribution of privileged action to workload plus initiating/approving authority |
| EAIMS-ADV-005 Adversarial Evaluation Coverage | OPS-02 | Evaluation tied to credible adversarial scenarios |
| EAIMS-ADV-006 Runtime Abuse Evidence | OPS-03 | Investigation-grade evidence for blocked/anomalous/unauthorized actions |
| EAIMS-ADV-007 Adversarial Incident Containment | OPS-04 | Containment of agent authority, credentials, tools, memory and dependencies |
| EAIMS-ADV-008 AI Threat Intelligence Disposition | GOV-02 | Closed-loop review of relevant AI threat intelligence |
| MSP-005 strengthened | TEC-02 | Fallback/exit plus material provider concentration or single-provider exposure |
| MSP-008 strengthened | TEC-02 | Composite dependency trace plus concentration/single-point exposure |
| EAIMS-ADV-010 Synthetic Identity & Representation Control | GOV-05 | Authorization and escalation for synthetic identity/influence exposure |

## Existing controls intentionally not duplicated

EAIMS 1.0 already includes strong controls for:

- autonomy classification;
- permission envelopes;
- action auditability;
- no authority exceedance;
- operational suspension;
- delegation boundaries;
- tool inventory;
- agent identity;
- no silent authority expansion;
- agent action logs;
- monitoring blind spots;
- incident routes;
- suspension testing;
- misuse monitoring;
- provider dependency and composite dependency trace.

EAIMS 1.1 should strengthen these concepts only where the new semantics are materially distinct.

## Assessment migration

### Existing 1.0.x assessment

A completed 1.0.x assessment remains a valid 1.0.x result.

### Reassessment under 1.1

When reassessing under 1.1:

1. reuse valid evidence that remains within scope and validity;
2. assess the 9 new ADV candidate requirements plus strengthened MSP-005/MSP-008 semantics, and any 1.0 requirements invalidated by material change;
3. activate agent-specific additions only where the system is action-taking/agentic as defined by the profile;
4. activate synthetic-identity controls only where that exposure is material;
5. document threat-intelligence review at organizational scope where relevant;
6. do not infer satisfaction from a 1.0 maturity score alone.

## Gate migration

The proposed G3-13 through G3-17 checks extend the existing Autonomous / Agentic gate family. They do not replace G3-01 through G3-12.

A 1.0 G3 PASS does not automatically imply a 1.1 G3 PASS.

## Compatibility objective

A conformant EAIMS 1.1 implementation should be able to:

- identify the source specification version of an assessment;
- reproduce a 1.0.x assessment without applying 1.1-only requirements;
- clearly separate historical results from migrated/reassessed results;
- explain which new requirements changed the result;
- preserve evidence provenance across migration.
