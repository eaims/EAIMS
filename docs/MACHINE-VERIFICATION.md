# Critical Machine Verification — FC16

EAIMS classifies requirements by machine verifiability. FC16 implements an explicit verifier for every **critical MV1/MV2 SHALL/SHALL_NOT** requirement.

## Policy

A machine-verification rule is a deterministic check over a structured verification context. It demonstrates that a machine-checkable condition can be evaluated consistently; it does not by itself prove that an enterprise control is effective in production.

Each critical MV1/MV2 requirement has:

1. a stable requirement ID;
2. an explicit operator and semantic input path in `spec/machine-verification.yaml`;
3. a positive executable test;
4. a negative executable test.

Supported FC16 operators are intentionally small: `truthy`, `nonempty`, `enum`, and `all_nonempty`. Domain-specific executable engines (APE, HAB, evidence cutoff, risk/gates) remain separate when richer semantics are required.

## Coverage

- Critical MV1/MV2: **33**
- Explicit machine rules: **33**
- Rule coverage: **100%**

This is requirement-level design verification, not empirical validation of the control in a real organization.
