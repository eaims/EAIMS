# EAIMS 1.1 Draft — AI Threat Intelligence Operating Protocol

> Non-normative implementation guidance supporting candidate requirement EAIMS-ADV-008.

## Purpose

Convert relevant external AI threat intelligence into traceable enterprise decisions. Reading reports alone is not evidence of mature operation.

## Closed loop

`Source -> Triage -> Exposure mapping -> Decision -> Action -> Verification -> Learning`

## Minimum operating record

Each material threat-intelligence item should record:

- source;
- publication/event date;
- reviewer;
- affected AI systems or "none identified";
- relevant tactic/risk pattern;
- exposure rationale;
- disposition;
- owner;
- due date where action is required;
- resulting control/test/monitoring change;
- verification evidence;
- closure date.

## Disposition states

- **ACTION_REQUIRED** — material exposure exists and a change is required.
- **MONITOR** — exposure is plausible but no immediate control change is justified.
- **ACCEPTED** — exposure is understood and explicitly accepted by appropriate authority.
- **NOT_APPLICABLE** — no relevant exposure; rationale retained.
- **NEEDS_ANALYSIS** — insufficient information; owner assigned.
- **SUPERSEDED** — later intelligence materially replaces the item.

## Suggested source classes

- AI provider threat-intelligence reports;
- national cybersecurity agencies;
- NIST and comparable public risk/security guidance;
- OWASP GenAI/agentic security publications;
- MITRE ATLAS;
- major cloud/security threat-intelligence teams;
- relevant vendor advisories;
- sector-specific ISAC/CSIRT intelligence where available.

EAIMS does not require any specific commercial provider.

## Maturity interpretation

### L2
Threat information is consumed informally by individuals.

### L3
Relevant sources, review cadence, ownership and disposition records are defined.

### L4
Material findings are regularly mapped to inventory, tests, controls and monitoring; closure is measured.

### L5
The organization adapts threat models, controls and assurance priorities based on observed external and internal threat evidence, and verifies the effect of those changes.

## Anti-patterns

- subscribing to threat feeds with no review ownership;
- collecting reports with no inventory mapping;
- closing findings as "not relevant" without rationale;
- changing controls without linking the change to the triggering threat evidence;
- treating only cyber exploits as AI threat intelligence while ignoring agentic abuse, identity, influence, surveillance, model/tool supply-chain and autonomy risks.
