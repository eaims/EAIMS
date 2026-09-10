"""Compatibility helpers for the published EAIMS v0.2.1 CLI contract.

These functions preserve the existing ``eaims validate|score|report`` behavior while
EAIMS 1.0 introduces ``eaims assess`` and the new executable specification model.
They are intentionally isolated and must not be used to score EAIMS 1.0 fixtures.
"""
from __future__ import annotations

from collections import Counter
from html import escape
from typing import Any

LEGACY_VERSION = "0.2.1"
DIMENSIONS = {
    "1": "Strategy and Leadership",
    "2": "Value and Portfolio Management",
    "3": "Data and Knowledge Readiness",
    "4": "AI Engineering and Architecture",
    "5": "Infrastructure and Platforms",
    "6": "MLOps, LLMOps, and Lifecycle Operations",
    "7": "Governance, Risk, Security, and Responsible AI",
    "8": "Organization, Talent, and Culture",
    "9": "Adoption, Process Transformation, and Change",
}
CAPABILITIES = {f"{d}.{c}" for d in range(1, 10) for c in range(1, 4)}
CRITICAL_DIMENSIONS = {"3", "6", "7"}
CONFIDENCE = {"low", "medium", "high"}


class LegacyAssessmentError(ValueError):
    pass


def _indicative_level(score: float) -> int:
    if score < 0.5: return 0
    if score < 1.5: return 1
    if score < 2.5: return 2
    if score < 3.5: return 3
    if score < 4.5: return 4
    return 5


def validate_legacy_assessment(data: dict[str, Any], *, require_complete: bool = True) -> list[str]:
    errors: list[str] = []
    if data.get("standard") != "EAIMS": errors.append("standard must be EAIMS")
    if data.get("version") != LEGACY_VERSION: errors.append(f"version must be {LEGACY_VERSION}")
    for field in ("organization", "assessment_date", "assessment_type", "scope"):
        if not data.get(field): errors.append(f"{field} is required")
    rows = data.get("capability_scores")
    if not isinstance(rows, list): return errors + ["capability_scores must be an array"]
    seen: set[str] = set()
    for i, row in enumerate(rows):
        label = f"capability_scores[{i}]"
        cid = row.get("capability_id")
        if cid not in CAPABILITIES:
            errors.append(f"{label}.capability_id is unknown")
            continue
        if cid in seen: errors.append(f"duplicate capability_id {cid}")
        seen.add(cid)
        if row.get("not_applicable") is True:
            if not str(row.get("exclusion_rationale", "")).strip():
                errors.append(f"{cid} exclusion_rationale is required")
            continue
        score = row.get("score")
        if type(score) is not int or not 0 <= score <= 5: errors.append(f"{cid} score must be an integer from 0 to 5")
        if row.get("confidence") not in CONFIDENCE: errors.append(f"{cid} confidence must be low, medium, or high")
        if type(score) is int and score >= 3 and not row.get("evidence_ids"):
            errors.append(f"{cid} at Level 3+ requires at least one evidence_id")
    if require_complete:
        missing = sorted(CAPABILITIES - seen)
        if missing: errors.append("missing capabilities: " + ", ".join(missing))
    return errors


def score_legacy_assessment(data: dict[str, Any], *, require_complete: bool = True) -> dict[str, Any]:
    errors = validate_legacy_assessment(data, require_complete=require_complete)
    if errors: raise LegacyAssessmentError("; ".join(errors))
    scored = [r for r in data["capability_scores"] if not r.get("not_applicable")]
    dimension_scores: dict[str, float] = {}
    for did, name in DIMENSIONS.items():
        values = [r["score"] for r in scored if r["capability_id"].startswith(did + ".")]
        if values: dimension_scores[name] = sum(values) / len(values)
    if not dimension_scores: raise LegacyAssessmentError("at least one capability must be scored")
    aggregate = sum(dimension_scores.values()) / len(dimension_scores)
    indicative = _indicative_level(aggregate)
    final = indicative
    gate_adjustments: list[str] = []
    for did in sorted(CRITICAL_DIMENSIONS):
        name = DIMENSIONS[did]
        if dimension_scores.get(name, 0) < 2 and final > 3:
            final = 3
            gate_adjustments.append(f"Level capped at 3 because {name} is below 2.0")
    if final == 5 and any(value < 4 for value in dimension_scores.values()):
        final = 4
        gate_adjustments.append("Level 5 denied because at least one dimension is below 4.0")
    counts = Counter(r["confidence"] for r in scored)
    total = len(scored)
    low_share = counts["low"] / total if total else 1.0
    return {
        "standard": "EAIMS", "version": LEGACY_VERSION, "organization": data["organization"],
        "assessment_date": data["assessment_date"], "assessment_type": data["assessment_type"],
        "scope": data["scope"], "dimension_scores": {k: round(v, 4) for k, v in dimension_scores.items()},
        "aggregate_score": round(aggregate, 4), "indicative_level": indicative, "final_level": final,
        "gate_adjustments": gate_adjustments,
        "confidence_counts": {key: counts[key] for key in ("low", "medium", "high")},
        "low_confidence_share": round(low_share, 4), "provisional": low_share > (1 / 3),
        "excluded_capabilities": [r["capability_id"] for r in data["capability_scores"] if r.get("not_applicable")],
        "complete": len(data["capability_scores"]) == 27,
    }


def legacy_markdown_report(result: dict[str, Any]) -> str:
    lines = [
        f"# EAIMS Assessment — {result['organization']}", "",
        f"- **Version:** {result['version']}", f"- **Date:** {result['assessment_date']}",
        f"- **Type:** {result['assessment_type']}", f"- **Scope:** {result['scope']}",
        f"- **Aggregate score:** {result['aggregate_score']:.2f}",
        f"- **Final maturity level:** {result['final_level']}",
        f"- **Provisional:** {'Yes' if result['provisional'] else 'No'}", "",
        "## Dimension profile", "", "| Dimension | Score |", "|---|---:|",
    ]
    lines += [f"| {name} | {score:.2f} |" for name, score in result["dimension_scores"].items()]
    lines += ["", "## Gate adjustments", ""]
    lines += [f"- {item}" for item in result["gate_adjustments"]] or ["- None"]
    lines += ["", "> EAIMS is decision support, not certification, compliance, safety, or legal assurance.", ""]
    return "\n".join(lines)


def legacy_html_report(result: dict[str, Any]) -> str:
    rows = "".join(f"<tr><td>{escape(k)}</td><td>{v:.2f}</td></tr>" for k, v in result["dimension_scores"].items())
    gates = "".join(f"<li>{escape(x)}</li>" for x in result["gate_adjustments"]) or "<li>None</li>"
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>EAIMS report</title><style>body{{font:16px system-ui;max-width:900px;margin:40px auto;padding:0 20px;color:#172033}}table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;border-bottom:1px solid #d9dfeb;text-align:left}}.score{{font-size:3rem;font-weight:750;color:#155eef}}.note{{background:#f2f5fa;padding:16px;border-radius:10px}}</style><h1>EAIMS Assessment</h1><h2>{escape(result['organization'])}</h2><div class="score">Level {result['final_level']}</div><p>Aggregate: {result['aggregate_score']:.2f} · Version {escape(result['version'])}</p><table><thead><tr><th>Dimension</th><th>Score</th></tr></thead><tbody>{rows}</tbody></table><h2>Gate adjustments</h2><ul>{gates}</ul><p class="note">EAIMS is decision support, not certification, compliance, safety, or legal assurance.</p></html>'''
