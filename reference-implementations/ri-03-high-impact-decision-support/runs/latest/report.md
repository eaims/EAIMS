# EAIMS Assessment Report — ASM-RI03-001

- Specification: `1.0.0-fc16`
- Report generated at: `2026-09-09T11:23:21Z`
- Evidence cutoff: `2026-09-09T08:00:00Z`
- Assessment type: `TARGETED`
- System: **Synthetic High-Impact Employment Decision Support**
- Derived risk band: **HIGH**
- Targeted assessment: **profile only; no enterprise-wide index produced**
- Autonomy debt: **NONE**
- Result hash: `12585c5116298770f307c1dad517bba92ff2f99dbe7e6c623f2c5eb8dc35d436`

## Coverage

- Capabilities in scope: **6**
- Applicable determinate ratio: **100%**
- Critical capabilities assessed: **False**
- Dimensions represented: **3/8**

## Dimension profile

| Dimension | Index |
|---|---:|
| GOV | 2.29 |
| OPS | 2.00 |
| PEO | 2.00 |

## Capability results

| Capability | Result | Confidence |
|---|---:|---:|
| OPS-02 | L2 | C4 |
| OPS-03 | L2 | C3 |
| GOV-02 | L2 | C4 |
| GOV-03 | L2 | C3 |
| GOV-05 | L3 | C3 |
| PEO-03 | L2 | C4 |

## Gate findings

- **G2-03 BREACH** — Final Authority Defined: Applicable control demonstrably not satisfied.

## Agent Permission Envelope

Not applicable.

## Human Accountability Boundary

- Final authority: **HUMAN**
- Human Reserved decisions: **1**
- Recourse available: **True**
- Intervention feasible: **True**
- **CRITICAL** — human_reserved_decision_executed_by_ai (`EVT-RI03-002`)

## Consistency findings

- **CRITICAL CONS-HAB-EXEC-001** — Human Accountability Boundary violation: human_reserved_decision_executed_by_ai

## Validation note

This result demonstrates deterministic execution of selected EAIMS rules. Synthetic reference implementations do not constitute empirical validation, certification, regulatory conformity, or production deployment assurance.
