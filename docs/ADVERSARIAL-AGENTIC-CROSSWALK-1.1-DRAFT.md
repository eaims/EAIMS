# EAIMS 1.1 Draft — Adversarial & Agentic Security Crosswalk

> **Non-normative development aid.** This document does not establish certification, equivalence, endorsement, legal compliance, or clause-level conformance with any referenced framework.

## Purpose

EAIMS is a maturity standard. It should measure whether an organization governs adversarial and agentic AI risk effectively without reproducing specialized security frameworks.

The crosswalk below identifies conceptual relationships only.

| EAIMS 1.1 candidate | NIST AI RMF / GenAI Profile | OWASP Agentic Applications 2026 | MITRE ATLAS | Threat-intelligence rationale |
|---|---|---|---|---|
| EAIMS-ADV-001 Adversarial Exposure Analysis | Govern / Map / Measure risk identification and lifecycle risk treatment | Agentic threat modeling and security-risk categories | AI adversary tactics/techniques and realized/demonstrated threats | Anthropic and GTIG report real-world malicious use and agentic automation |
| EAIMS-ADV-002 Blast Radius Assessment | Context-sensitive risk and impact analysis | Tool misuse, unsafe autonomy, unintended/unauthorized action | Impact, exfiltration, execution, privilege and agent-tool techniques | Agentic workflows can compress response windows and scale action |
| EAIMS-ADV-003 Agent Credential Boundary | Access/control risk treatment and secure deployment | Identity & privilege abuse; tool access boundaries | Credential access, privilege escalation, lateral movement | Real-world agent-enabled operations increase the importance of bounded authority |
| EAIMS-ADV-004 Agent Privilege Attribution | Accountability, traceability and monitoring | Identity, privilege and observability controls | Execution, credential access, command/control and agent invocation | Runtime attribution is needed to reconstruct autonomous or semi-autonomous actions |
| EAIMS-ADV-005 Adversarial Evaluation Coverage | Measure / Manage; evaluation of GAI-specific risks | Agentic security testing and abuse scenarios | ATLAS-informed red teaming and threat assessment | Threat reports show misuse patterns evolve beyond normal functional testing |
| EAIMS-ADV-006 Runtime Abuse Evidence | Monitoring, measurement and risk-response evidence | Runtime controls, telemetry and detection | Detection-relevant adversary activity across agentic systems | Reduced human latency makes runtime evidence and alerting materially more important |
| EAIMS-ADV-007 Adversarial Incident Containment | Manage and incident-response improvement | Agent/tool containment, privilege restriction, recovery | Execution, persistence, command/control, exfiltration and impact pathways | Threat actors increasingly use AI as an operational layer, so containment must include agent authority and dependencies |
| EAIMS-ADV-008 AI Threat Intelligence Disposition | Govern / Map / Manage emerging risk | Continuous security improvement | ATLAS living knowledge base and observed techniques | Anthropic and GTIG publish changing real-world TTPs that can invalidate prior assumptions |
| MSP-005 / MSP-008 strengthened dependency semantics | Third-party/lifecycle risk and supply-chain context | Agentic supply-chain exposure | Resource development, initial access, model/tool ecosystem abuse | GTIG reports supply-chain compromise involving AI coding assistants/scanners |
| EAIMS-ADV-010 Synthetic Identity & Representation Control | Human/social impact and GAI risk governance | Context-dependent deceptive/unsafe agent behavior | Deepfake/external-harm and related influence-enabling techniques | Anthropic reports influence operations, synthetic personas, impersonation and surveillance abuse |

## Reference boundaries

### NIST

NIST AI RMF and NIST AI 600-1 provide broad risk-management functions and GenAI-specific risk guidance. EAIMS uses these as conceptual risk-management references and does not reproduce NIST controls or claim formal mapping completeness.

Reference:
https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

### OWASP

OWASP's Top 10 for Agentic Applications 2026 identifies critical security risks facing autonomous and agentic AI systems. EAIMS should assess whether an organization operationally governs relevant risks rather than becoming an application-security testing manual.

Reference:
https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/

### MITRE ATLAS

MITRE ATLAS is a living knowledge base of adversary tactics and techniques involving AI-enabled systems, including Generative AI and Agentic AI. EAIMS can use ATLAS to support threat-informed evaluation and red-team planning without copying its technique catalog.

Reference:
https://atlas.mitre.org/

### Anthropic Threat Intelligence

Anthropic's September 2026 report documents disrupted misuse across cyber operations, surveillance, influence operations, scams/fraud, biological misuse, conventional weapons, and illicit distillation. It includes cases where AI was used as an engineering workforce and operational component.

Reference:
https://www.anthropic.com/threat-intelligence-report-september-2026

### Google Threat Intelligence Group

GTIG's September 8, 2026 report describes adversaries moving from basic prompting to agentic workflows and AI-enabled automation, with sharply reduced human-in-the-loop latency and examples of agent-enabled credential-harvesting and software supply-chain abuse.

Reference:
https://cloud.google.com/blog/topics/threat-intelligence/from-prompting-to-autonomy-the-evolution-of-adversarial-ai

## EAIMS design rule

External references should inform:

`Threat / risk evidence -> EAIMS requirement -> evidence expectation -> maturity interpretation -> gate consequence`

They should not result in:

`External framework -> copied checklist -> duplicated standard`

This distinction keeps EAIMS focused on enterprise maturity, evidence, accountability, and adaptive governance.
