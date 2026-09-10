# EAIMS 1.0 assessment guide

## Choose the correct workflow

EAIMS 1.0 uses 8 dimensions, 30 capabilities and levels L1–L5. The v0.2.x questionnaire, browser interface and `validate`, `score`, `report` commands remain available for historical compatibility. Their results are not interchangeable with v1 results.

## Run a complete synthetic example

From a checkout of the repository, using Python 3.10 or later:

```bash
python -m pip install -e '.[test]'
eaims-validate
eaims validate-fixture reference-implementations/ri-02-enterprise-service-agent/input/fixture.yaml
eaims assess reference-implementations/ri-02-enterprise-service-agent/input/fixture.yaml --out run-output
```

Open `run-output/report.md` and `run-output/result.json`. This targeted example reports a financial permission-envelope violation and breached G3-04 and G3-10 gates. It produces no enterprise-wide maturity index. The breach is deliberately injected into synthetic data; the example is not a customer deployment.

A useful assessor response is to identify the action that exceeded authority, verify the source event and approved limit, assign an owner to investigate enforcement, and document retest evidence before reassessment. The engine reports the finding; it does not itself suspend a production agent or implement remediation.

## Prepare a real assessment input

Copy a reference fixture into a private working location and replace its synthetic values and evidence references. Define the assessment scope, system, risk profile and evidence cutoff before scoring.

- `assessment`: stable assessment identifier, FULL/PARTIAL/TARGETED scope type and a timezone-aware cutoff timestamp.
- `system` and `risk_profile`: the system context and the impact, autonomy, reversibility, scale and velocity classifications.
- `capabilities`: canonical capability IDs, applicability, observed anchors and completed operating/adaptation cycles.
- `evidence`: identifiable sources, evidence class, confidence, nature, validity and collection time. Quote YAML timestamps, for example `"2026-09-09T07:00:00Z"`.
- `requirement_results`: canonical requirement IDs, assessor determinations and supporting evidence references. SATISFIED SHALL/SHALL_NOT determinations require evidence references.
- `gate_inputs`: explicit PASS/BREACH/INCOMPLETE/NOT_APPLICABLE assertions, or actual booleans. Modeled automated G2/G3 findings take precedence over manual assertions.
- Agent or high-impact scenarios: supply the permission envelope, decision policy, events and relevant controls used by that scenario.

Use actual YAML booleans (`true`, `false`), not quoted boolean strings. Cycle counts are nonnegative integers. Financial values are finite nonnegative numbers, not strings or booleans; use consistent monetary units for the approved limit and events. Duplicate YAML keys, duplicate evidence/capability/requirement IDs and broken evidence references are rejected. Missing audit fields can still yield explicit incomplete-audit findings; do not interpret absent events as proof that controls operated.

Run `validate-fixture` before `assess`. Structural validity does not establish authenticity, completeness or effectiveness of organizational evidence. Additional contextual fields are preserved in input but may not be evaluated by the engine.

## Interpret the output

| Output | Meaning |
|---|---|
| `capability_results` | Awarded level or an explicit INDETERMINATE / NOT_APPLICABLE / NOT_ASSESSED state, with available rationale and traces |
| `dimension_profile` | Profile across represented dimensions |
| `gate_results` | Explicit control gate results; inspect breaches and incomplete gates separately from maturity scores |
| `coverage` | Scope and determinate-evidence coverage used by the engine |
| `enterprise_index` | Available only for FULL assessments meeting the implemented coverage criteria |
| `indicative_scoped_index` | Scoped indicator for PARTIAL assessments or insufficiently covered FULL assessments |
| `result_hash` | Deterministic hash of the result content before adding the hash field; not a digital signature or proof of evidence authenticity |

TARGETED assessments produce no overall index. A FULL assessment must contain all 30 canonical capabilities; the engine also checks critical-capability assessment, determinate coverage and dimension representation. A maturity result does not establish certification, compliance or production safety. Keep gate findings, confidence and evidence limitations visible when sharing the report.

## Automate review exit checks

```bash
eaims review summarize validation/review-workflow-fixture.yaml --out review-output --fail-on-unmet
```

The included fixture is synthetic and only demonstrates the workflow. Replace it with actual review records and resolutions for real review decisions. Independent-review classification is supplied by the record; the engine does not authenticate a reviewer's independence.

With `--fail-on-unmet`, exit 0 means the modeled review exit criteria were met; exit 1 means they were not met. In both cases reports are written. Invalid review input exits 2. Without the option, successful report generation retains exit 0 even if criteria are unmet. Duplicate review IDs, finding keys and resolution IDs are rejected rather than overwritten.

Assessment commands exit 1 for rejected fixtures and 2 for loading/parsing errors. Use the shared package data root (`EAIMS_ROOT` when needed); review commands now resolve installed schemas in the same way as assessment commands.

## Contracts and evidence boundary

Use [assessment-fixture-v1.schema.json](../schemas/assessment-fixture-v1.schema.json) and [assessment-result-v1.schema.json](../schemas/assessment-result-v1.schema.json) for v1 integration. Semantic checks in the engine supplement the input schema. Legacy schemas remain unchanged.

Some machine rules inspect supplied flags or references. They do not independently inspect enterprise access controls, logs or monitoring systems. Production evidence collection, empirical calibration and independent multi-organization validation remain outside the demonstrated boundary; see [VALIDATION.md](../VALIDATION.md).
