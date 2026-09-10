# EAIMS Schemas

| Workflow | Input | Output |
|---|---|---|
| EAIMS 1.0 reference engine (`validate-fixture`, `assess`) | `assessment-fixture-v1.schema.json` | `assessment-result-v1.schema.json` |
| Legacy v0.2.x (`validate`, `score`, `report`) | `assessment-input.schema.json` / `assessment.schema.json` | `assessment-result.schema.json` |
| Review | `review-feedback.schema.json`, `review-resolution.schema.json` | Review summary and findings ledger |

The v1 input schema checks the types of supported executable fields. Additional properties remain allowed for context and extensions; their presence does not mean the engine evaluates them. The engine separately validates canonical references, applicability rationales, evidence references, assessment scope and cutoff timestamps. Finite-number and recursive-data checks run before schema validation. JSON Schema date-time validation requires a format checker.

The v1 result schema describes the stable report envelope and FULL/PARTIAL/TARGETED index semantics. It is not proof of evidence authenticity or enterprise control effectiveness. The normative provenance remains `1.0.0-fc16`.

See the [v1 assessment guide](../docs/ASSESSMENT-V1.md). Keep confidential evidence in protected repositories and publish only appropriate references.
