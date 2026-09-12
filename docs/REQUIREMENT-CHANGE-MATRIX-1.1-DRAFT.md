# EAIMS 1.1 Draft — Requirement Change Matrix

> Development review artifact. This matrix explains why each candidate requirement exists and how it relates to EAIMS 1.0.x.

| Candidate | Existing 1.0.x coverage | Residual gap addressed | New evidence expectation | Compatibility |
|---|---|---|---|---|
| EAIMS-ADV-001 Adversarial Exposure Analysis | EAIMS-RSK-001/002/004; generic impact/risk factors and reclassification | 1.0 does not explicitly require adversarial manipulation, misuse/abuse, privilege and dependency exposure to be part of the risk analysis | threat model, abuse-case analysis, adversarial exposure review | additive to GOV-02 |
| EAIMS-ADV-002 Blast Radius Assessment | EAIMS-AUT-002/005/007/008; permission, authority, reversibility, velocity/scale | 1.0 constrains authority but does not explicitly require a maximum-credible-impact boundary for compromised/manipulated agent action | blast-radius analysis, segmentation/action limits, transaction or reach bounds | additive to GOV-04 |
| EAIMS-ADV-003 Agent Credential Boundary | EAIMS-AGT-006/007; agent identity and no silent authority expansion | observable identity is not equivalent to scoped/revocable authorization and separation from unrestricted administrator authority | IAM/workload identity configuration, credential scope, revocation test | additive to TEC-04 |
| EAIMS-ADV-004 Agent Privilege Attribution | EAIMS-AUT-004, EAIMS-AGT-003/006, EAIMS-MON-003 | existing traceability does not explicitly bind privileged action to both agent identity and initiating/approving authority | privileged action log, approval/delegation identity trace | additive to TEC-04 |
| EAIMS-ADV-005 Adversarial Evaluation Coverage | EAIMS-EVL-001/002 and L5 adversarial-evidence language | 1.0 requires evaluation but does not make credible adversarial scenarios an explicit material-system requirement | adversarial evaluation plan/results, scenario coverage, remediation record | additive to OPS-02 |
| EAIMS-ADV-006 Runtime Abuse Evidence | EAIMS-MON-001/003/007/008; monitoring and agent-action logs | action logging does not explicitly require evidence of blocked/anomalous/unauthorized/policy-violating actions adequate for investigation | blocked-action records, anomaly/security telemetry, correlation context | additive to OPS-03 |
| EAIMS-ADV-007 Adversarial Incident Containment | EAIMS-INC-001/005/006/008; incident route, containment, suspension and learning | 1.0 does not explicitly enumerate containment of agent authority, credentials, tools, memory, external actions and affected dependencies | containment runbook/test, credential revoke evidence, tool isolation, memory/session containment | additive to OPS-04 |
| EAIMS-ADV-008 AI Threat Intelligence Disposition | EAIMS-RSK-004, EAIMS-LRN-001/002/005; reassessment and learning | no explicit closed-loop requirement to consume relevant AI threat intelligence and disposition findings against inventory/controls/tests | source review record, exposure mapping, disposition decision, control/test update | additive to GOV-02 |
| EAIMS-ADV-009 AI Dependency Concentration | EAIMS-MSP-002/005/006/008; provider dependencies, exit and dependency chains | dependency tracing does not explicitly require concentration/single-provider systemic-risk analysis | dependency graph, concentration analysis, exit/fallback evidence | additive to TEC-02 |
| EAIMS-ADV-010 Synthetic Identity & Representation Control | EAIMS-RAI-001/005; harm categories and use-case-specific responsible-AI controls | 1.0 does not explicitly address persistent synthetic personas, impersonation, organizational representation or scaled persuasive automation | authorization, representation policy, disclosure/provenance controls, monitoring/escalation | conditionally additive to GOV-05 |

## Decision tests

A candidate requirement should remain in EAIMS 1.1 only if all of the following are true:

1. **Distinct semantics:** the requirement cannot be satisfied merely by pointing to an existing 1.0 requirement with no additional evidence.
2. **Enterprise maturity relevance:** it tests organizational governance/operation rather than prescribing low-level offensive or defensive technique.
3. **Evidenceability:** an assessor can identify supporting, counter, absence, or contextual evidence.
4. **Risk proportionality:** applicability can be bounded to material exposure.
5. **Non-duplication:** specialized NIST/OWASP/MITRE content is referenced, not copied.
6. **Backward compatibility:** historical 1.0.x results remain interpretable without retroactive regrading.

## Candidate consolidation decisions

### Keep separate

- **ADV-002** should remain distinct because blast radius is an assurance/impact boundary, not merely a permission envelope.
- **ADV-003** should remain distinct because observable agent identity is weaker than bounded credential authority.
- **ADV-008** should remain distinct because periodic AI-specific threat-intelligence disposition is an organizational closed loop not currently explicit in 1.0.
- **ADV-010** should remain conditional and distinct because synthetic representation/influence exposure is not universal.

### Potential future merge after validation

- **ADV-004** could eventually be folded into strengthened AGT-006/MON-003 semantics if empirical review shows a separate requirement adds no assessor value.
- **ADV-006** could eventually be folded into MON-003/MON-007 if "investigation-grade abuse evidence" can be expressed cleanly without weakening existing log semantics.
- **ADV-009** could eventually become an extension of MSP-008 if concentration risk is consistently treated as part of dependency trace.

No consolidation should occur before worked-case and inter-rater validation.
