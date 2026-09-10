# RI-02 — Enterprise Autonomous Service Agent

Synthetic, executable EAIMS reference implementation for an enterprise customer-service agent that can read/write CRM data and issue low-value refunds.

The approved Agent Permission Envelope allows autonomous refunds up to 100 monetary units. The fixture deliberately injects one 250-unit refund to demonstrate that EAIMS can distinguish **a documented control** from **observed operational non-conformance**.

RI-02 exercises:

- A3 approved vs A4 observed autonomy drift
- Agent Permission Envelope (APE)
- financial/action limits
- action-level auditability
- operational suspension testing
- memory policy
- Human Accountability Boundary
- G0/G1/G2/G3 inheritance under high velocity/scale escalation
- deterministic machine-derived G3 gate results
- qualitative Autonomy Debt

This is a synthetic reference implementation, not a production deployment or external empirical validation.
