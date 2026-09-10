# RC Review Operations

This workflow operationalizes review without converting review into endorsement or empirical validation.

## Intake

1. Preserve the submitted review record unchanged.
2. Validate it against `schemas/review-feedback.schema.json`.
3. Record the exact artifact hash/version reviewed.
4. Expand every finding into the findings ledger.

## Disposition

Every BLOCKER and MAJOR finding requires a resolution record. A MAJOR may be accepted without code/spec change only when the acceptance rationale is explicit and traceable. A BLOCKER must be resolved before RC exit.

The original reviewer record is immutable. Maintainer responses are stored separately in resolution records.

## Re-review

A finding resolution should set `requires_rereview: true` when the correction materially changes architecture, maturity semantics, scoring, gates, evidence rules, HAB/autonomy semantics, or public claims.

## RC exit

Review is complete for RC only when the protocol exit rule is met. This is a design-review milestone, not evidence of empirical validity, certification, regulatory conformity, production validation, or inter-rater reliability.
