# RFC 0004 — Adversarial and Agentic AI Governance for EAIMS 1.1

**Status:** Draft  
**Target:** EAIMS 1.1  
**Change class:** Normative candidate  
**Compatibility:** Additive-first; EAIMS 1.0.x remains frozen and valid

## 1. Problem

EAIMS 1.0 already addresses agent permissions, tool inventories, action auditability, monitoring, incident response, responsible AI, supply-chain assurance, and misuse monitoring. Recent threat intelligence nevertheless shows a material change in operating conditions: AI systems are increasingly used not only as assistants but as autonomous or semi-autonomous operators, orchestration layers, surveillance engineering workforces, influence-operation infrastructure, and attack accelerators.

This creates maturity questions that are not yet explicit enough in EAIMS 1.0:

- whether organizations consume AI-specific threat intelligence and translate it into control changes;
- whether agent identities and privileged credentials are governed independently from human identities;
- whether the blast radius of an AI or agent is measured before deployment;
- whether misuse and abuse resilience is tested against realistic adversarial behavior;
- whether high-autonomy systems produce runtime evidence sufficient for reconstruction and containment;
- whether synthetic identity, impersonation, provenance, and influence risks are governed;
- whether external provider and agent-tool dependency concentration can create systemic exposure.

## 2. Evidence base

This RFC is informed by public, non-proprietary sources and does not reproduce protected standards text.

### Primary threat-intelligence evidence

- Anthropic, *Detecting and countering misuse of AI: September 2026* — documents increasingly autonomous cyber operations, multi-agent orchestration, persistent campaign memory, surveillance engineering, influence operations, and abuse patterns.
  - https://www.anthropic.com/threat-intelligence-report-september-2026
- Google Threat Intelligence Group, *From Prompting to Autonomy — The Evolution of Adversarial AI* (September 2026) — reports transition from prompting to agentic workflows, compressed defender response windows, credential-harvesting automation, and supply-chain abuse involving AI systems.
  - https://cloud.google.com/blog/topics/threat-intelligence/from-prompting-to-autonomy-the-evolution-of-adversarial-ai

### Risk and security references

- NIST AI RMF Generative AI Profile (NIST AI 600-1) — generative-AI-specific lifecycle risks and risk-management actions.
  - https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- NIST Secure Software Development Practices for Generative AI and Dual-Use Foundation Models — secure development practices for AI model and system producers and acquirers.
  - https://www.nist.gov/publications/secure-software-development-practices-generative-ai-and-dual-use-foundation-models-ssdf
- OWASP Top 10 for Agentic Applications 2026 — agentic security risks involving goal hijacking, tool misuse, identity/privilege abuse, supply-chain exposure, and unsafe execution.
  - https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- MITRE ATLAS — public knowledge base for adversarial threats to AI-enabled systems.
  - https://atlas.mitre.org/

## 3. Design principles

The proposal SHALL preserve the following EAIMS principles:

1. EAIMS measures organizational maturity; it does not become a penetration-testing standard.
2. Existing security frameworks are referenced rather than duplicated.
3. Evidence of operation is stronger than evidence of policy alone.
4. Risk determines control intensity.
5. Autonomy, privilege, reach, reversibility, and detectability affect required assurance.
6. EAIMS 1.0.x results remain interpretable and are not retroactively invalidated.

## 4. Proposed additions

### 4.1 Adversarial AI exposure profile

Introduce an assessment construct that records, at minimum:

- autonomy level;
- privilege level;
- external-action capability;
- data sensitivity;
- reach/scale;
- reversibility;
- detectability;
- dependency concentration;
- potential blast radius.

A candidate assurance relationship is:

`Required Assurance = f(Impact, Autonomy, Privilege, Reach, Reversibility, Detectability)`

This is a governance relationship, not a mandatory numeric formula in 1.1 unless validated.

### 4.2 AI identity and privileged access

Strengthen existing autonomy and architecture requirements so that material action-taking agents demonstrate:

- unique workload/agent identity where technically feasible;
- least-privilege and scoped credentials;
- short-lived or bounded credentials where supported;
- separation of human and agent privileges;
- traceable credential issuance and revocation;
- emergency revocation;
- privileged-action attribution.

### 4.3 Blast-radius governance

For material action-taking systems, require documented analysis of the maximum credible scope of harm or unauthorized action arising from:

- model failure;
- prompt/context manipulation;
- tool compromise;
- credential compromise;
- agent delegation;
- automation loops;
- provider or dependency compromise.

Blast-radius controls SHOULD include segmentation, rate/action limits, approval boundaries, transaction caps, sandboxing, isolation, and kill/suspend capability as applicable.

### 4.4 AI misuse and abuse resilience

Elevate misuse monitoring from adoption telemetry into an adversarial governance concern.

Candidate requirements:

- documented abuse/misuse scenarios for material systems;
- adversarial test coverage proportionate to risk;
- defined detection and escalation routes;
- retained abuse-control evidence;
- post-incident control updates;
- explicit handling of prompt injection, tool misuse, data exfiltration, impersonation, unauthorized surveillance/profiling, and policy-evasion scenarios where relevant.

### 4.5 AI threat intelligence and emerging risk

Introduce an organizational maturity requirement to:

- identify relevant AI-specific threat-intelligence sources;
- review them at a defined cadence;
- map material findings to the AI inventory and risk register;
- update controls, tests, monitoring, or deployment restrictions when exposure changes;
- retain evidence of disposition, including "not applicable" decisions.

At higher maturity, this becomes continuous or event-driven rather than periodic.

### 4.6 Runtime evidence for autonomous systems

For material agentic systems, policy documents alone SHALL NOT be sufficient evidence for high maturity.

Expected runtime evidence may include:

- agent/tool/action logs;
- approval records;
- privilege changes;
- delegation traces;
- model/provider/version identifiers where available;
- blocked actions;
- alerts and escalations;
- suspension/recovery tests;
- incident reconstruction artifacts.

### 4.7 Synthetic identity, provenance, and influence risk

Where the assessed scope generates or distributes synthetic content, represents people/organizations, performs persuasive communication, or automates public-facing communication, governance SHOULD address:

- impersonation controls;
- disclosure/representation policy;
- content provenance or authenticity mechanisms where appropriate;
- brand/persona authorization;
- mass-amplification controls;
- audience targeting restrictions;
- monitoring for deceptive or unauthorized representation.

This area is context-dependent and SHALL NOT be activated for systems that do not create a material synthetic-identity or influence exposure.

### 4.8 AI dependency and concentration risk

Extend sourcing and supply-chain assessment beyond model/provider recording to include dependency graphs for material systems:

`Business process -> AI application -> agent -> model -> retrieval/context -> tool/MCP/API -> data source -> external provider`

Organizations SHOULD identify concentration or single-provider dependencies that could create systemic operational, security, sovereignty, or exit risk.

## 5. Proposed gate evolution

EAIMS 1.0 G3 (Autonomous / Agentic) already provides a strong baseline. EAIMS 1.1 should extend it rather than replace it.

Candidate new or strengthened gate checks:

- agent/workload identity defined;
- privileged credentials scoped and revocable;
- blast radius assessed;
- runtime action evidence retained;
- adversarial/misuse testing completed for material agentic systems;
- dependency/tool trust boundaries documented;
- emergency suspension tested;
- material external communication and transaction pathways bounded.

A separate "adversarial" gate family SHOULD be introduced only if validation shows that extending G2/G3 cannot represent the risk cleanly.

## 6. Maturity interpretation

Proposed interpretation for adversarial resilience:

- **L1 — Initial:** adversarial AI risk is largely unmanaged or addressed reactively.
- **L2 — Emerging:** selected risks and technical controls are identified, but coverage is inconsistent.
- **L3 — Defined:** material systems have documented threat scenarios, identity/permission boundaries, response routes, and evidence requirements.
- **L4 — Managed:** runtime monitoring, adversarial evaluation, incident evidence, and control effectiveness are measured.
- **L5 — Adaptive:** threat intelligence, incidents, red-team findings, dependency changes, and observed abuse continuously update controls and assurance requirements.

## 7. Compatibility

EAIMS 1.1 SHOULD be additive-first:

- preserve 1.0 capability IDs wherever possible;
- avoid renumbering stable requirements unless unavoidable;
- introduce new requirement IDs only for genuinely new semantics;
- provide a 1.0 -> 1.1 migration/crosswalk;
- keep 1.0.x reference implementations reproducible;
- do not reinterpret historical 1.0.x assessment results.

## 8. Validation plan

Before normative adoption:

1. map each proposed change to current 1.0 requirements to remove duplicates;
2. create positive and negative fixtures for material agentic systems;
3. test inter-rater interpretation with at least two assessor scenarios;
4. test backwards compatibility against all 1.0 reference implementations;
5. add machine-verifiable rules only where deterministic verification is defensible;
6. document unresolved judgment areas as MV3/MV4 rather than forcing false automation;
7. perform a standards/threat-intelligence crosswalk and legal/IP review.

## 9. Out of scope

EAIMS 1.1 will not:

- prescribe exploit procedures;
- reproduce OWASP, NIST, ISO, or MITRE controls;
- define offensive cyber techniques;
- certify that an AI system is secure or safe;
- imply endorsement by any referenced organization.

## 10. Decision requested

Approve this RFC as the design basis for an EAIMS 1.1 development profile, followed by requirement-level gap analysis, fixtures, validation, and public review before any normative freeze.
