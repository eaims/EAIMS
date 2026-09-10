# Multi-Assessor Workflow — FC16

FC16 preserves each assessor's original requirement decision and explicitly classifies disagreement. It never averages conflicting judgments into a synthetic midpoint.

Workflow:

1. Validate each assessor record against the normative assessor protocol.
2. Group records by requirement ID.
3. Classify disagreement as `NONE`, `EVIDENCE`, `APPLICABILITY`, or `MATERIAL`.
4. Where resolution is required, preserve all original records.
5. Create a separate resolution record with resolver, final decision, rationale, evidence references, all considered assessor IDs, and timestamp.
6. Export long-form assessor records for later inter-rater analysis.

The synthetic worked cases demonstrate mechanics only. They do **not** establish inter-rater reliability, and FC16 does not report kappa/ICC from synthetic cases as validation evidence.
