# EAIMS 1.0 — Capability-Specific Anchor Eligibility (FC16)

FC16 replaces generic E1–E4-only maturity progression for canonical EAIMS capabilities with an explicit eligibility rule for each of the 150 maturity anchors.

Each anchor can constrain an award using five independently traceable conditions:

1. **Anchor observation** — whether the capability-specific anchor is actually observed.
2. **Required normative requirements** — SHALL/SHALL NOT requirements assigned to that maturity threshold.
3. **Minimum evidence class** — E1 for L2, E2 for L3, E3 for L4 and E4 for L5 unless a future capability-specific override is adopted.
4. **Operating/adaptation cycles** — L4 currently requires two demonstrated operating cycles; L5 also requires at least one evidenced adaptation cycle.
5. **Counter-evidence** — material or critical operational contradictions can prevent higher maturity even when supporting artifacts exist.

The generic cycle counts are **design defaults**, not empirically calibrated constants. They remain provisional through RC evaluation.

## Higher-order evidence

Evidence of advanced practice is never discarded merely because a lower prerequisite is absent. The engine reports `higher_order_observations_preserved` while constraining the awarded maturity to the highest cumulatively eligible level.

## Cross-capability dependencies

FC16 introduces a deliberately small explicit dependency catalog rather than hidden weighting. Hard dependencies may constrain a level only when both capabilities are assessed in scope. Supporting dependencies create findings and do not silently alter maturity.

Current hard examples include:

- GOV-04 L4 → OPS-02 at least L3.
- TEC-04 L4 → GOV-04 at least L3 for agentic contexts.
- VAL-03 L4 → OPS-02 at least L3 for material pilots.

These rules are stored in `spec/anchor-eligibility.yaml` and are testable and auditable.
