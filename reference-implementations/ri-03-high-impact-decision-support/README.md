# RI-03 — High-Impact Decision Support

Synthetic targeted reference implementation for a high-impact employment decision-support system.

The policy explicitly reserves the final adverse employment decision to a human. The fixture then injects one operational event in which the AI improperly executes that Human Reserved decision. FC16 checks that machine-observed execution can override a manually asserted G2-03 PASS, reports a Human Accountability Boundary violation, and constrains the affected maturity claims.

This is a synthetic reference case, not a production deployment or empirical validation study.
