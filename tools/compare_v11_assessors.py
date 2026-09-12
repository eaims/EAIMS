#!/usr/bin/env python3
"""Compare two independent EAIMS 1.1 assessor response files."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import yaml

CASES = ("IR-01","IR-02","IR-03","IR-04","IR-05","IR-06","IR-07")
EXACT_FIELDS = ("applicability","result","gate_result")
CRITICAL_CASES = {"IR-02","IR-04"}

class ComparisonError(Exception):
    pass

def load(path: Path):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ComparisonError(f"{path}: response must be a mapping")
    if data.get("independent_completion_confirmed") is not True:
        raise ComparisonError(f"{path}: independent_completion_confirmed must be true")
    cases = data.get("cases")
    if not isinstance(cases, dict) or set(cases) != set(CASES):
        raise ComparisonError(f"{path}: cases must contain exactly {', '.join(CASES)}")
    return data

def compare(a, b):
    if a.get("assessor_id") == b.get("assessor_id"):
        raise ComparisonError("assessor_id values must be different")

    rows=[]
    critical_blockers=[]
    exact_agreement=0

    for case in CASES:
        left=a["cases"][case]
        right=b["cases"][case]
        disagreements=[field for field in EXACT_FIELDS if left.get(field) != right.get(field)]
        agreed=not disagreements
        if agreed:
            exact_agreement += 1
        blocker=bool(disagreements and case in CRITICAL_CASES)
        if blocker:
            critical_blockers.append(case)
        rows.append({
            "case":case,
            "exact_agreement":agreed,
            "disagreement_fields":disagreements,
            "confidence_a":left.get("confidence"),
            "confidence_b":right.get("confidence"),
            "critical_freeze_blocker":blocker,
        })

    return {
        "assessor_a":a.get("assessor_id"),
        "assessor_b":b.get("assessor_id"),
        "exact_agreement_cases":exact_agreement,
        "total_cases":len(CASES),
        "agreement_ratio":round(exact_agreement/len(CASES),4),
        "critical_freeze_blockers":critical_blockers,
        "candidate_freeze_review_result":"BLOCKED" if critical_blockers else "NO_CRITICAL_DISAGREEMENT",
        "cases":rows,
    }

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("assessor_a",type=Path)
    parser.add_argument("assessor_b",type=Path)
    parser.add_argument("--json",action="store_true")
    args=parser.parse_args(argv)
    try:
        result=compare(load(args.assessor_a),load(args.assessor_b))
    except ComparisonError as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(result,indent=2))
    else:
        print(f"Agreement: {result['exact_agreement_cases']}/{result['total_cases']} ({result['agreement_ratio']:.1%})")
        print(f"Critical blockers: {', '.join(result['critical_freeze_blockers']) or 'none'}")
        for row in result["cases"]:
            mark="AGREE" if row["exact_agreement"] else "DISAGREE"
            fields=",".join(row["disagreement_fields"]) or "-"
            print(f"{row['case']}: {mark} fields={fields} blocker={row['critical_freeze_blocker']}")
    return 1 if result["critical_freeze_blockers"] else 0

if __name__=="__main__":
    raise SystemExit(main())
