# EAIMS Adversarial & Agentic Governance Profile — Development Draft

> **Development profile for EAIMS 1.1.** This document is non-normative until adopted through the RFC and release process. EAIMS 1.0.x remains the stable normative baseline.

## Purpose

This profile helps assess whether an organization can create value with AI while controlling risks introduced by autonomous action, adversarial manipulation, abuse, privileged access, synthetic identity, and fast-changing AI threat activity.

It complements existing EAIMS 1.0 capabilities rather than creating a parallel security framework.

## 1. Assessment lens

For each material AI system, assess:

| Factor | Question |
|---|---|
| Impact | What is the credible consequence of failure or abuse? |
| Autonomy | Can the system recommend, decide, act, delegate, or persist without human approval? |
| Privilege | What systems, identities, data, tools, or transactions can it access? |
| Reach | How many users, records, systems, customers, or external parties can it affect? |
| Reversibility | How difficult is it to undo an action or decision? |
| Detectability | How quickly would harmful or unauthorized behavior be detected? |
| Dependency | Which models, providers, tools, MCP servers, APIs, context stores, and data sources are trusted? |
| Blast radius | What is the maximum credible scope of damage from failure, compromise, or manipulation? |

## 2. Evidence expectations

High maturity should favor operational evidence over policy-only evidence.

### Supporting evidence

- agent/workload identity inventory;
- permission and credential configuration;
- dependency graph;
- tool inventory and trust boundaries;
- adversarial evaluation results;
- prompt-injection and tool-abuse test results where relevant;
- action and delegation logs;
- approval records;
- blocked-action records;
- incident timelines;
- suspension/kill-switch test evidence;
- threat-intelligence review records;
- control-change records;
- synthetic-content or impersonation controls where relevant.

### Counter-evidence

Examples include:

- shared administrator credentials used by agents;
- unrestricted tool access;
- undocumented external actions;
- no action logging for privileged agents;
- no tested suspension capability;
- runtime behavior that exceeds the approved permission envelope;
- material threat findings reviewed but not dispositioned;
- policy-only claims with no observable enforcement;
- synthetic personas or public-facing automation without authorization or representation rules.

## 3. Runtime evidence principle

For material action-taking AI, EAIMS should distinguish:

**Declared control** — policy, architecture document, procedure, approval.

**Implemented control** — configuration, code, permission boundary, test.

**Observed control** — runtime logs, blocked actions, alerts, incident evidence, successful suspension/recovery.

For L4/L5 claims, observed evidence should normally be present for controls that can produce runtime evidence.

## 4. Agent identity and privilege

Material agents should have identifiable and bounded authority.

Expected characteristics include:

- workload identity distinguishable from the initiating human where feasible;
- least privilege;
- scoped credentials;
- bounded credential lifetime where supported;
- traceable delegation;
- explicit external-action permissions;
- revocation and emergency suspension;
- logging sufficient to attribute privileged actions.

## 5. Blast-radius classes — experimental

The following classes are an experimental assessment aid, not yet normative:

| Class | Typical exposure |
|---|---|
| B0 | No external action; informational output only |
| B1 | Read-only access to bounded internal information |
| B2 | Modification of low-risk internal records within a bounded domain |
| B3 | External communication or workflow actions affecting third parties |
| B4 | Privileged system changes, broad enterprise actions, or material transactions |
| B5 | Safety-critical, systemic, irreversible, or high-consequence action |

A higher blast-radius class should increase evidence, testing, monitoring, approval, and recovery expectations.

## 6. Threat-intelligence loop

A mature organization should operate a closed loop:

`Threat intelligence -> Exposure mapping -> Risk decision -> Control/test update -> Runtime observation -> Incident/learning -> Updated threat model`

Evidence should show not merely that reports were read, but whether material findings changed organizational action.

## 7. Adversarial evaluation

Evaluation should be proportionate to context and may include:

- indirect/direct prompt injection;
- malicious or compromised context;
- unauthorized tool requests;
- privilege escalation attempts;
- data exfiltration attempts;
- agent-goal manipulation;
- unsafe delegation;
- memory poisoning;
- dependency/tool compromise assumptions;
- impersonation or deceptive-output scenarios;
- policy-evasion attempts.

EAIMS should evaluate whether the organization governs and tests these risks; detailed attack procedures belong in specialized security frameworks.

## 8. Synthetic identity and influence exposure

Activate this area when AI systems:

- impersonate or represent people or organizations;
- create persistent personas;
- produce public-facing persuasive content at scale;
- automate outreach or audience targeting;
- generate media whose origin could be materially misunderstood.

Assessment should consider authorization, disclosure, provenance, amplification limits, monitoring, and escalation.

## 9. Dependency graph

For material systems, the organization should be able to identify a dependency path such as:

`Business process -> AI application -> agent -> model -> context/retrieval -> tool/API/MCP -> data source -> external provider`

The graph should support change-impact analysis, provider exit planning, incident containment, and concentration-risk review.

## 10. Relationship to external references

This development profile is informed by public material from:

- NIST AI RMF and the Generative AI Profile;
- NIST secure software development guidance for generative AI;
- OWASP GenAI and Agentic Application guidance;
- MITRE ATLAS;
- Anthropic threat-intelligence reporting;
- Google Threat Intelligence Group reporting.

References are informative only. EAIMS does not claim equivalence, certification, endorsement, or clause-level compliance with those sources.
