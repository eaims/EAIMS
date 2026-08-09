#!/usr/bin/env python3
"""
EAIMS Paper 01 sensitivity analysis.

Purpose
-------
Reproduce controlled computational sensitivity experiments over the three
fictional EAIMS assessment fixtures without changing the normative v0.2
reference engine.

This script intentionally treats custom dimension weighting and alternative
gate thresholds as EXTERNAL SENSITIVITY SIMULATIONS. EAIMS v0.2 reference
scoring uses equal weighting and a fixed critical threshold of 2.0.

Run from repository root:
    python research/paper-01/sensitivity_analysis.py

Output:
    research/paper-01/sensitivity_results.csv
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = [
    ROOT / "examples" / "fictional-manufacturer.assessment.json",
    ROOT / "examples" / "fictional-bank.assessment.json",
    ROOT / "examples" / "fictional-cloud-company.assessment.json",
]

DIMENSIONS = {str(i): i for i in range(1, 10)}
CRITICAL_BASELINE = {"3", "6", "7"}

GATE_THRESHOLDS = [1.5, 2.0, 2.5, 3.0, 3.5]
CONFIDENCE_THRESHOLDS = [0.20, 0.25, 1 / 3, 0.40, 0.50]

WEIGHT_SCENARIOS = {
    "equal": {},
    "strategy_x2": {"1": 2.0},
    "governance_x2": {"7": 2.0},
    "operations_x2": {"6": 2.0},
}

CRITICAL_SET_SCENARIOS = {
    "baseline_3_6_7": {"3", "6", "7"},
    "plus_infrastructure": {"3", "5", "6", "7"},
    "plus_talent": {"3", "6", "7", "8"},
}

def indicative_level(score: float) -> int:
    if score < 0.5:
        return 0
    if score < 1.5:
        return 1
    if score < 2.5:
        return 2
    if score < 3.5:
        return 3
    if score < 4.5:
        return 4
    return 5

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def dimension_scores(data: dict) -> dict[str, float]:
    out = {}
    rows = [r for r in data["capability_scores"] if not r.get("not_applicable")]
    for did in DIMENSIONS:
        vals = [
            r["score"] for r in rows
            if r["capability_id"].startswith(did + ".")
        ]
        if vals:
            out[did] = sum(vals) / len(vals)
    return out

def weighted_aggregate(ds: dict[str, float], weights: dict[str, float]) -> float:
    total = 0.0
    denom = 0.0
    for did, score in ds.items():
        w = weights.get(did, 1.0)
        total += score * w
        denom += w
    return total / denom

def apply_gate(
    aggregate: float,
    ds: dict[str, float],
    *,
    critical_set: set[str],
    threshold: float,
) -> tuple[int, bool, int]:
    indicative = indicative_level(aggregate)
    final = indicative
    gate_active = any(ds.get(did, 0.0) < threshold for did in critical_set)

    if gate_active and final > 3:
        final = 3

    if final == 5 and any(v < 4.0 for v in ds.values()):
        final = 4

    gate_impact = indicative - final
    return final, gate_active, gate_impact

def low_share(data: dict) -> float:
    rows = [r for r in data["capability_scores"] if not r.get("not_applicable")]
    if not rows:
        return 1.0
    low = sum(1 for r in rows if r.get("confidence") == "low")
    return low / len(rows)

def emit(rows: list[dict]) -> None:
    output = Path(__file__).with_name("sensitivity_results.csv")
    fields = [
        "fixture", "experiment", "configuration",
        "aggregate_score", "indicative_level",
        "gate_active", "gate_impact", "final_level",
        "low_confidence_share", "provisional",
    ]
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {output}")

def main() -> None:
    rows = []

    for path in EXAMPLES:
        data = load(path)
        fixture = data["organization"]
        ds = dimension_scores(data)
        base_low = low_share(data)

        # A — critical-gate threshold sensitivity
        for threshold in GATE_THRESHOLDS:
            agg = weighted_aggregate(ds, {})
            final, active, impact = apply_gate(
                agg, ds, critical_set=CRITICAL_BASELINE, threshold=threshold
            )
            rows.append({
                "fixture": fixture,
                "experiment": "gate_threshold",
                "configuration": f"{threshold:g}",
                "aggregate_score": f"{agg:.4f}",
                "indicative_level": indicative_level(agg),
                "gate_active": str(active).lower(),
                "gate_impact": impact,
                "final_level": final,
                "low_confidence_share": f"{base_low:.4f}",
                "provisional": str(base_low > (1/3)).lower(),
            })

        # B — dimension-weight sensitivity (external simulation)
        for name, weights in WEIGHT_SCENARIOS.items():
            agg = weighted_aggregate(ds, weights)
            final, active, impact = apply_gate(
                agg, ds, critical_set=CRITICAL_BASELINE, threshold=2.0
            )
            rows.append({
                "fixture": fixture,
                "experiment": "dimension_weight",
                "configuration": name,
                "aggregate_score": f"{agg:.4f}",
                "indicative_level": indicative_level(agg),
                "gate_active": str(active).lower(),
                "gate_impact": impact,
                "final_level": final,
                "low_confidence_share": f"{base_low:.4f}",
                "provisional": str(base_low > (1/3)).lower(),
            })

        # C — confidence threshold sensitivity
        base_agg = weighted_aggregate(ds, {})
        base_final, active, impact = apply_gate(
            base_agg, ds, critical_set=CRITICAL_BASELINE, threshold=2.0
        )
        for threshold in CONFIDENCE_THRESHOLDS:
            rows.append({
                "fixture": fixture,
                "experiment": "confidence_threshold",
                "configuration": f"{threshold:.4f}",
                "aggregate_score": f"{base_agg:.4f}",
                "indicative_level": indicative_level(base_agg),
                "gate_active": str(active).lower(),
                "gate_impact": impact,
                "final_level": base_final,
                "low_confidence_share": f"{base_low:.4f}",
                "provisional": str(base_low > threshold).lower(),
            })

        # D — critical-set membership sensitivity
        for name, critical_set in CRITICAL_SET_SCENARIOS.items():
            agg = weighted_aggregate(ds, {})
            final, active, impact = apply_gate(
                agg, ds, critical_set=critical_set, threshold=2.0
            )
            rows.append({
                "fixture": fixture,
                "experiment": "critical_set",
                "configuration": name,
                "aggregate_score": f"{agg:.4f}",
                "indicative_level": indicative_level(agg),
                "gate_active": str(active).lower(),
                "gate_impact": impact,
                "final_level": final,
                "low_confidence_share": f"{base_low:.4f}",
                "provisional": str(base_low > (1/3)).lower(),
            })

    emit(rows)

if __name__ == "__main__":
    main()
