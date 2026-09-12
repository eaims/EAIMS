# EAIMS 1.1 Draft — Adversarial & Agentic Assessor Protocol

> Development protocol for RFC 0004. Non-normative until adopted.

## 1. Objective

Assess whether adversarial and agentic controls are demonstrated in the actual operating context, rather than inferred from policy intent or product claims.

## 2. Assessment sequence

1. Confirm system scope and materiality.
2. Determine applicability using the 1.1 activation overlay.
3. Preserve all relevant 1.0 counter-evidence.
4. Collect declared, implemented, and observed evidence.
5. Evaluate each applicable ADV requirement.
6. Evaluate candidate G3 extensions where activated.
7. Record unresolved ambiguity as INSUFFICIENT_EVIDENCE or CONDITIONALLY_APPLICABLE rather than assuming PASS/N/A.
8. Record material conflicts and escalation.
9. Document effect on maturity and gate status separately.

## 3. Required assessor questions

### ADV-001 — Adversarial Exposure Analysis
- Which adversarial manipulations are credible in this context?
- Does the threat model include context, tool, credential, dependency, misuse and abuse exposure where relevant?
- What evidence shows the analysis was used in decisions?

### ADV-002 — Blast Radius
- What is the maximum credible scope of harmful or unauthorized action?
- Which technical or procedural bounds limit that scope?
- What happens when those bounds fail?

### ADV-003 — Agent Credential Boundary
- Which identity does the agent execute as?
- Are credentials scoped and revocable?
- Can the agent inherit unrestricted human/admin authority?
- Has revocation been tested where material?

### ADV-004 — Privilege Attribution
- Can a privileged action be traced to agent/workload identity?
- Can it be traced to initiating/approving authority?
- Can delegation chains be reconstructed?

### ADV-005 — Adversarial Evaluation
- Which credible attack or misuse scenarios are tested?
- Are results retained?
- Did failures produce remediation and retest?

### ADV-006 — Runtime Abuse Evidence
- Are blocked/rejected/anomalous actions retained?
- Can investigators reconstruct the sequence and authorization context?
- Are policy violations linked to alerts/escalation?

### ADV-007 — Adversarial Incident Containment
- Can credentials be revoked independently?
- Can tools/external actions be disabled?
- Can memory/session state be contained where relevant?
- Does suspension remove authority or only stop one process?

### ADV-008 — AI Threat Intelligence Disposition
- Which external sources are considered relevant?
- Who reviews them and at what cadence?
- Which findings were mapped to the AI inventory?
- What was changed, accepted, deferred, or declared not applicable?

### Candidate MSP-005 / MSP-008 — Dependency Concentration & Trace
- Which critical external providers, tools, APIs, MCP servers, context stores, models, or services are required?
- Is any single dependency a material point of failure, control concentration, sovereignty exposure, or exit constraint?
- Is fallback or exit credible and tested proportionately?
- Is the composite dependency chain traceable where material?
- ADV-009 is development-history only and must not be scored separately in candidate-freeze review.

### ADV-010 — Synthetic Identity & Representation
- Does the AI represent a real person, organization, or persistent persona?
- Who authorizes that representation?
- Are disclosure/provenance and amplification controls appropriate to context?
- How are impersonation or deceptive-use incidents escalated?

## 4. Evidence quality

For L3:
- evidence should show defined and implemented governance.

For L4:
- evidence should show repeated operational use and measured control effectiveness.

For L5:
- evidence should show adaptation caused by observed incidents, threat intelligence, evaluation findings, or material environmental change.

## 5. Prohibited shortcuts

An assessor must not:

- equate policy existence with control operation;
- infer NOT_APPLICABLE from missing context;
- overwrite negative evidence with newer supporting evidence without resolution history;
- treat vendor security claims as sufficient internal assurance;
- treat a successful kill-switch demo as proof that credentials, tools and sessions were contained;
- infer adversarial evaluation from ordinary functional testing;
- infer low blast radius solely from low financial value if privacy, safety, scale or reputational impact remains material.

## 6. Assessment output

The assessment record should contain:

- applicability decision and rationale;
- requirement result;
- evidence references;
- counter-evidence;
- unresolved uncertainty;
- gate effect;
- remediation owner and due state where applicable;
- reassessment trigger.
