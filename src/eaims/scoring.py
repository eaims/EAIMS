"""Deterministic EAIMS v0.2 scoring and validation."""
from __future__ import annotations

from collections import Counter
from typing import Any

VERSION = "0.2.0"
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


class AssessmentError(ValueError):
    """Raised when an assessment cannot be scored safely."""


def _indicative_level(score: float) -> int:
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


def validate_assessment(data: dict[str, Any], *, require_complete: bool = True) -> list[str]:
    """Return validation errors without mutating input."""
    errors: list[str] = []
    if data.get("standard") != "EAIMS":
        errors.append("standard must be EAIMS")
    if data.get("version") != VERSION:
        errors.append(f"version must be {VERSION}")
    for field in ("organization", "assessment_date", "assessment_type", "scope"):
        if not data.get(field):
            errors.append(f"{field} is required")
    rows = data.get("capability_scores")
    if not isinstance(rows, list):
        return errors + ["capability_scores must be an array"]
    seen: set[str] = set()
    for i, row in enumerate(rows):
        label = f"capability_scores[{i}]"
        cid = row.get("capability_id")
        if cid not in CAPABILITIES:
            errors.append(f"{label}.capability_id is unknown")
            continue
        if cid in seen:
            errors.append(f"duplicate capability_id {cid}")
        seen.add(cid)
        if row.get("not_applicable") is True:
            if not str(row.get("exclusion_rationale", "")).strip():
                errors.append(f"{cid} exclusion_rationale is required")
            continue
        score = row.get("score")
        if type(score) is not int or not 0 <= score <= 5:
            errors.append(f"{cid} score must be an integer from 0 to 5")
        if row.get("confidence") not in CONFIDENCE:
            errors.append(f"{cid} confidence must be low, medium, or high")
        if type(score) is int and score >= 3 and not row.get("evidence_ids"):
            errors.append(f"{cid} at Level 3+ requires at least one evidence_id")
    if require_complete:
        missing = sorted(CAPABILITIES - seen)
        if missing:
            errors.append("missing capabilities: " + ", ".join(missing))
    return errors


def score_assessment(data: dict[str, Any], *, require_complete: bool = True) -> dict[str, Any]:
    """Score an EAIMS assessment, applying critical gates and confidence rules."""
    errors = validate_assessment(data, require_complete=require_complete)
    if errors:
        raise AssessmentError("; ".join(errors))
    scored = [r for r in data["capability_scores"] if not r.get("not_applicable")]
    dimension_scores: dict[str, float] = {}
    for did, name in DIMENSIONS.items():
        values = [r["score"] for r in scored if r["capability_id"].startswith(did + ".")]
        if values:
            dimension_scores[name] = sum(values) / len(values)
    if not dimension_scores:
        raise AssessmentError("at least one capability must be scored")
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
    confidence = {key: counts[key] for key in ("low", "medium", "high")}
    low_share = counts["low"] / total if total else 1.0
    exclusions = [r["capability_id"] for r in data["capability_scores"] if r.get("not_applicable")]
    return {
        "standard": "EAIMS",
        "version": VERSION,
        "organization": data["organization"],
        "assessment_date": data["assessment_date"],
        "assessment_type": data["assessment_type"],
        "scope": data["scope"],
        "dimension_scores": {k: round(v, 4) for k, v in dimension_scores.items()},
        "aggregate_score": round(aggregate, 4),
        "indicative_level": indicative,
        "final_level": final,
        "gate_adjustments": gate_adjustments,
        "confidence_counts": confidence,
        "low_confidence_share": round(low_share, 4),
        "provisional": low_share > (1 / 3),
        "excluded_capabilities": exclusions,
        "complete": len(data["capability_scores"]) == 27,
    }
