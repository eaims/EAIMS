# EAIMS 1.1 Draft — Requirement Consolidation Decision Record

> Development decision record for RFC 0004. The objective is to minimize duplicate semantics before normative freeze.

## Decision summary

After comparison against EAIMS 1.0 requirements, the current recommendation is:

| Candidate | Decision | Rationale |
|---|---|---|
| ADV-001 | KEEP | Adversarial exposure is not explicitly required by existing generic risk analysis. |
| ADV-002 | KEEP | Blast radius is distinct from permission boundaries and reversibility. |
| ADV-003 | KEEP | Agent identity does not equal bounded credential/authorization scope. |
| ADV-004 | MERGE CANDIDATE | Strong overlap with AGT-006 + AGT-003 + AUT-004 + MON-003; likely better as strengthened attribution semantics than a permanent new requirement. |
| ADV-005 | KEEP | Existing evaluation requirements do not explicitly mandate adversarial scenario coverage. |
| ADV-006 | MERGE CANDIDATE | Could be integrated into MON-003/MON-007 if investigation-grade abuse evidence becomes explicit. |
| ADV-007 | KEEP | Existing incident/suspension controls do not explicitly require authority/credential/tool/memory containment. |
| ADV-008 | KEEP | No existing closed-loop AI-specific threat-intelligence disposition requirement. |
| ADV-009 | MERGE CANDIDATE | Could strengthen MSP-008/005 with concentration/systemic dependency semantics. |
| ADV-010 | KEEP, CONDITIONAL | Synthetic identity/representation exposure is materially distinct and context-dependent. |

## Proposed post-validation consolidation path

### ADV-004 -> strengthen existing requirements

Possible target semantics:

- AGT-006 Agent Identity: include workload identity sufficient for execution attribution.
- AGT-003 Delegation Traceability: require reconstruction of initiating/delegating authority.
- MON-003 Agent Action Logs: require correlation between privileged action, agent identity, and approving/initiating authority.

Keep ADV-004 during development until worked-case testing confirms no distinct assessor value is lost.

### ADV-006 -> strengthen monitoring semantics

Possible target semantics:

- MON-003 Agent Action Logs: explicitly include blocked, rejected, anomalous, unauthorized and policy-violating actions where material.
- MON-007 Log Retention: require retention sufficient for reconstruction of material incidents.

Keep ADV-006 during development because runtime abuse evidence is central to the 1.1 design and must not disappear through premature consolidation.

### ADV-009 -> strengthen sourcing/dependency semantics

Possible target semantics:

- MSP-008 Composite Dependency Trace: include material tool/API/MCP/context dependencies.
- MSP-005 Fallback or Exit Strategy: include concentration and single-provider exposure.
- MSP-002 Provider Dependency: distinguish dependency identification from concentration analysis.

Keep ADV-009 until pilot review determines whether concentration risk is consistently assessable as a separate maturity requirement.

## Freeze criterion

No merge candidate should be consolidated until:

1. at least two worked cases demonstrate equivalent assessment outcomes;
2. no gate loses a distinct control consequence;
3. evidence expectations remain explicit;
4. inter-rater interpretation does not degrade;
5. migration semantics remain explainable.
