# EAIMS 1.1 — Final Consolidation Decision (Draft)

> Development decision for candidate freeze. Non-normative until accepted through RFC 0004.

## Decision

### ADV-004 — KEEP

**Reason:** Existing 1.0 controls establish agent identity, delegation traceability, action auditability, and action logs, but none explicitly require a privileged action to be correlated to both:

1. the executing agent/workload identity; and
2. the initiating or approving authority.

This is a distinct accountability property with direct G3 gate value.

### ADV-006 — KEEP

**Reason:** Existing action logging and retention requirements do not explicitly require retention of blocked, rejected, anomalous, unauthorized, or policy-violating action evidence sufficient for investigation.

This is a distinct operational assurance property and should remain separately assessable.

### ADV-009 — MERGE INTO MSP-005 / MSP-008

**Reason:** Provider/dependency concentration is important, but a permanent standalone requirement would split one sourcing/dependency concern across overlapping IDs.

Candidate 1.1 semantics should therefore:

- strengthen **MSP-005** to cover fallback/exit plus material concentration exposure;
- strengthen **MSP-008** to cover material tool/API/MCP/context/external-service dependencies and concentration/single-point exposure.

The development identifier **EAIMS-ADV-009** should remain in historical draft artifacts for traceability but should not enter the final normative 1.1 ID set if this decision is accepted.

## Resulting candidate requirement delta

EAIMS 1.1 candidate adds **9 new ADV requirements** and strengthens **2 existing MSP requirements**.

This is preferred over adding 10 permanent new IDs because it preserves conceptual cohesion and limits framework inflation.

## Compatibility

- No existing 1.0 requirement ID is removed or renumbered.
- MSP-005/MSP-008 changes are semantic strengthening only for 1.1 assessments.
- Historical 1.0.x results remain valid under their original version.
- Migration records should identify when MSP-005/MSP-008 were reassessed under 1.1 semantics.
