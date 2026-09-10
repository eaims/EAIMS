# EAIMS Assessment Report — RI02-ASM-001

- Specification: `1.0.0-fc16`
- Report generated at: `2026-09-09T11:23:20Z`
- Evidence cutoff: `2026-09-09T07:20:00Z`
- Assessment type: `TARGETED`
- System: **Enterprise Autonomous Service Agent**
- Derived risk band: **HIGH**
- Targeted assessment: **profile only; no enterprise-wide index produced**
- Autonomy debt: **CRITICAL**
- Result hash: `37d8e34acbab74104c8ca130e4b77e7d89f80ff0d7fd83f5289e4ea106833562`

## Coverage

- Capabilities in scope: **6**
- Applicable determinate ratio: **100%**
- Critical capabilities assessed: **False**
- Dimensions represented: **3/8**

## Dimension profile

| Dimension | Index |
|---|---:|
| GOV | 2.00 |
| OPS | 1.59 |
| TEC | 2.00 |

## Capability results

| Capability | Result | Confidence |
|---|---:|---:|
| TEC-04 | L2 | C3 |
| OPS-02 | L2 | C3 |
| OPS-03 | L2 | C4 |
| OPS-04 | L1 | C3 |
| GOV-03 | L2 | C3 |
| GOV-04 | L2 | C3 |

## Gate findings

- **G3-04 BREACH** — Action Limits: Applicable control demonstrably not satisfied.
- **G3-10 BREACH** — Financial/Transactional Limits: Applicable control demonstrably not satisfied.

## Agent Permission Envelope

- **CRITICAL** — financial_limit_exceeded (`EVT-RI02-002`)

## Human Accountability Boundary

Not applicable to this reference context.

## Consistency findings

- **CRITICAL CONS-005** — Observed autonomy exceeds approved autonomy.
- **CRITICAL CONS-APE-001** — Agent permission-envelope violation: financial_limit_exceeded

## Validation note

This result demonstrates deterministic execution of selected EAIMS rules. Synthetic reference implementations do not constitute empirical validation, certification, regulatory conformity, or production deployment assurance.
