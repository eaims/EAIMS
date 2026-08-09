# EAIMS v0.2 Scoring Methodology

## 1. Capability scores

Each of 27 capabilities receives an integer score from 0 to 5 using the highest maturity anchor fully supported by evidence. If evidence is incomplete, select the lower defensible score. In executable conformance, Level 3–5 scores require at least one evidence identifier.

## 2. Confidence

Each scored capability receives Low, Medium, or High confidence. Confidence never raises or multiplies maturity. Report counts and shares separately. More than one-third Low-confidence scores makes the result **provisional**.

## 3. Dimension score

EAIMS v0.2 uses equal weighting across all in-scope capabilities within each dimension:

`sum(in-scope capability scores) / count(in-scope capabilities)`

Exclusions require a documented not-applicable rationale and change the denominator. Missing responses are not zero and cannot be silently excluded.

Alternative capability-weighting schemes are experimental and are not part of executable conformance in EAIMS v0.2.

## 4. Aggregate score

EAIMS v0.2 uses equal weighting across all scored dimensions:

`sum(dimension scores) / count(scored dimensions)`

Calculations retain full precision; display rounding occurs only after aggregation.

Alternative dimension-weighting schemes are experimental and are not part of executable conformance in EAIMS v0.2.

## 5. Indicative level

| Aggregate | Level |
|---:|---:|
| 0.00–0.49 | 0 |
| 0.50–1.49 | 1 |
| 1.50–2.49 | 2 |
| 2.50–3.49 | 3 |
| 3.50–4.49 | 4 |
| 4.50–5.00 | 5 |

## 6. Critical gates

Data and Knowledge Readiness; MLOps, LLMOps, and Lifecycle Operations; and Governance, Risk, Security, and Responsible AI are critical dimensions.

- If any critical dimension is below 2.0, the final level cannot exceed Level 3.
- Level 5 requires every dimension to be at least 4.0.

Report the aggregate, indicative level, final level, and each gate adjustment separately. Additional human adjustments may only reduce the final level and must be justified in writing outside the reference engine.

## 7. Target state

Target maturity should be strategically relevant, economically justified, risk appropriate, and achievable in the roadmap horizon. Level 5 is not automatically the correct target.

## 8. Limitations

Scores are decision support, not certification, compliance, system safety, security, ethical acceptability, investment performance, or benchmark standing. Comparison requires compatible versions, scope, profiles, assessment modes, and confidence.
