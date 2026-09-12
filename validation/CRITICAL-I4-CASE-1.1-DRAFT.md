# EAIMS 1.1 Draft — Critical I4 Worked Case

> Non-normative validation case for adversarial/agentic gate consequences.

## Case CRIT-01 — Autonomous production-control agent

A material production-control agent operates at **I4 / A4 / R4 / S4 / D3**.

The agent can:
- modify production scheduling and routing;
- issue commands to operational technology through a bounded gateway;
- communicate with external suppliers;
- persist task state;
- invoke approved planning and execution tools.

The system has a documented permission envelope and tool inventory, but the following failures are present:

1. no documented maximum credible blast-radius analysis;
2. adversarial evaluation has not tested malicious context/tool output;
3. runtime logs record successful actions but not blocked/rejected policy violations;
4. emergency process termination works, but external execution credentials remain valid after termination.

## Expected requirement interpretation

| Requirement | Expected result | Reason |
|---|---|---|
| ADV-001 | SATISFIED | Adversarial exposure is documented |
| ADV-002 | NOT_SATISFIED | No blast-radius analysis |
| ADV-003 | PARTIALLY_SATISFIED | Credentials are scoped but containment/revocation is incomplete |
| ADV-004 | SATISFIED | Privileged actions are attributable |
| ADV-005 | NOT_SATISFIED | Credible adversarial tool/context scenarios are untested |
| ADV-006 | NOT_SATISFIED | Blocked/rejected abuse evidence is not retained |
| ADV-007 | NOT_SATISFIED | Termination does not revoke execution authority |
| ADV-008 | SATISFIED | Relevant threat intelligence is reviewed and dispositioned |
| ADV-009 | SATISFIED | Critical dependencies and concentration are analyzed |
| ADV-010 | NOT_APPLICABLE | No synthetic identity/representation exposure |

## Expected gate consequences

### G3-13 — Blast Radius Assessed

**BREACH**

Because the system is I4, R4 and S4, the draft gate-effects policy triggers:

- deployment_block;
- scale_block;
- maturity_cap;
- mandatory_remediation;
- reassessment_required.

Expected maturity cap: **L3**.

### G3-14 — Privileged Agent Credentials Bounded

**BREACH or INCOMPLETE**, depending on evidence proving independent revocability.

If revocation is demonstrably unavailable, treat as **BREACH**:

- deployment_block;
- maturity cap **L2**;
- mandatory remediation;
- reassessment required.

### G3-15 — Adversarial Evaluation

**BREACH**

I4 and A4 activate the deployment-block condition.

Expected:
- deployment_block;
- scale_block;
- maturity cap **L3**;
- mandatory remediation;
- reassessment required.

### G3-16 — Runtime Abuse Evidence

**BREACH**

The system performs privileged actions and lacks evidence for rejected/blocked behavior.

Expected:
- scale_block;
- maturity cap **L3**;
- mandatory remediation.

Deployment blocking should be considered if the absence of evidence combines with detectability conditions severe enough to prevent establishing a safe operating boundary.

### G3-17 — Adversarial Incident Containment

**BREACH**

Process termination without credential/tool authority revocation is not containment.

Expected:
- deployment_block;
- maturity cap **L2**;
- mandatory remediation;
- reassessment required.

## Aggregate interpretation

The strictest maturity cap prevails: **L2**.

Deployment/scale restrictions are reported separately from maturity and are not converted into numeric penalties.

A high aggregate maturity score in unrelated capabilities cannot average away these gate effects.

## Validation purpose

This case tests that the 1.1 draft:

- treats critical systemic exposure differently from ordinary material AI;
- distinguishes process termination from authority containment;
- does not let missing adversarial evidence disappear inside aggregate scoring;
- applies the strictest gate consequence after indicative maturity calculation;
- preserves explicit deployment/scale consequences separately from maturity.
