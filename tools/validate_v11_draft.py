#!/usr/bin/env python3
"""Structural validator for the EAIMS 1.1 adversarial/agentic development package.

This tool validates only draft overlay integrity. It does not make EAIMS 1.1 normative
and does not alter or reinterpret the EAIMS 1.0.x canonical specification.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "profile": ROOT / "spec" / "adversarial-agentic-1.1-draft.yaml",
    "anchors": ROOT / "spec" / "adversarial-agentic-anchors-1.1-draft.yaml",
    "activation": ROOT / "spec" / "adversarial-agentic-activation-1.1-draft.yaml",
    "evidence": ROOT / "spec" / "adversarial-agentic-evidence-1.1-draft.yaml",
    "gate_effects": ROOT / "spec" / "adversarial-agentic-gate-effects-1.1-draft.yaml",
    "machine_verification": ROOT / "spec" / "adversarial-agentic-machine-verification-1.1-draft.yaml",
    "positive": ROOT / "validation" / "v11-adversarial-positive.yaml",
    "negative": ROOT / "validation" / "v11-adversarial-negative.yaml",
    "regression": ROOT / "validation" / "v11-reference-regression.yaml",
}

ALLOWED_LEVELS = {"L1", "L2", "L3", "L4", "L5"}
ALLOWED_APPLICABILITY = {
    "APPLICABLE",
    "NOT_APPLICABLE",
    "CONDITIONALLY_APPLICABLE",
    "NOT_ASSESSED",
}
ALLOWED_EFFECTS = {
    "critical_risk_flag",
    "maturity_cap",
    "scale_block",
    "deployment_block",
    "mandatory_remediation",
    "reassessment_required",
}


class ValidationError(Exception):
    pass


def load(name: str) -> Any:
    path = FILES[name]
    if not path.exists():
        raise ValidationError(f"missing required draft artifact: {path.relative_to(ROOT)}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate() -> list[str]:
    messages: list[str] = []

    profile = load("profile")
    anchors = load("anchors")
    activation = load("activation")
    evidence = load("evidence")
    effects = load("gate_effects")
    mv = load("machine_verification")
    positive = load("positive")
    negative = load("negative")
    regression = load("regression")

    require(profile.get("normative") is False, "draft profile must remain non-normative")
    require(profile.get("status") == "development_draft", "draft profile status must be development_draft")

    candidates = profile.get("candidate_requirements", [])
    ids = [r["requirement_id"] for r in candidates]
    require(len(ids) == len(set(ids)), "candidate requirement IDs must be unique")
    candidate_ids = set(ids)
    require(candidate_ids == {f"EAIMS-ADV-{i:03d}" for i in range(1, 11)}, "candidate ADV ID set is incomplete or unexpected")
    messages.append(f"candidate requirements: {len(candidate_ids)}")

    # Anchor coverage
    anchor_refs = {
        req
        for cap in anchors["capability_extensions"].values()
        for req in cap["requirement_minimum_levels"]
    }
    require(anchor_refs == candidate_ids, "anchor overlay must cover every candidate exactly")
    for cap in anchors["capability_extensions"].values():
        require(set(cap["requirement_minimum_levels"].values()).issubset(ALLOWED_LEVELS), "invalid maturity level in anchor overlay")
    messages.append("anchor coverage: complete")

    # Activation coverage
    require(set(activation["rules"]) == candidate_ids, "activation rules must cover every candidate exactly")
    for req_id, rule in activation["rules"].items():
        require(rule["default"] in ALLOWED_APPLICABILITY, f"{req_id}: invalid activation default")
        if "fallback" in rule:
            require(rule["fallback"] in ALLOWED_APPLICABILITY, f"{req_id}: invalid activation fallback")
    messages.append("activation coverage: complete")

    # Evidence coverage
    require(set(evidence["requirements"]) == candidate_ids, "evidence overlay must cover every candidate exactly")
    for req_id, item in evidence["requirements"].items():
        require(bool(item.get("supporting")), f"{req_id}: supporting evidence examples required")
        require(bool(item.get("counter")), f"{req_id}: counter-evidence examples required")
    messages.append("evidence coverage: complete")

    # Gate references/effects
    gate_extensions = profile["candidate_gate_extensions"]["G3"]["add_checks"]
    gate_ids = {g["gate_id"] for g in gate_extensions}
    require(gate_ids == {"G3-13", "G3-14", "G3-15", "G3-16", "G3-17"}, "unexpected G3 extension set")
    for gate in gate_extensions:
        require(set(gate["requirement_ids"]).issubset(candidate_ids), f"{gate['gate_id']}: unknown requirement reference")
    require(set(effects["gate_effects"]) == gate_ids, "gate effects must cover every candidate G3 extension")
    for gate_id, item in effects["gate_effects"].items():
        require(set(item.get("on_breach", [])).issubset(ALLOWED_EFFECTS), f"{gate_id}: unsupported gate effect")
        if "maturity_cap" in item:
            require(item["maturity_cap"] in ALLOWED_LEVELS, f"{gate_id}: invalid maturity cap")
    messages.append("gate references/effects: complete")

    # MV rules must match only candidates explicitly classified MV2.
    mv2_candidates = {r["requirement_id"] for r in candidates if r["machine_verifiability"] == "MV2"}
    mv_ids = {r["requirement_id"] for r in mv["rules"]}
    require(mv_ids == mv2_candidates, "draft machine-verification coverage must equal MV2 candidate set")
    messages.append(f"candidate MV2 rules: {len(mv_ids)}")

    # Fixtures
    for name, fixture in (("positive", positive), ("negative", negative)):
        require(set(fixture["requirements"]) == candidate_ids, f"{name} fixture must cover all candidates")
        require(set(fixture["expected_gate_extensions"]) == gate_ids, f"{name} fixture must cover all G3 extensions")
    messages.append("positive/negative fixtures: complete")

    # Reference regression
    refs = regression["reference_implementations"]
    require(set(refs) == {"RI-01", "RI-02", "RI-03"}, "reference regression must cover RI-01/02/03")
    for ref_id, item in refs.items():
        require(item.get("expected_1_0_mutation") is False, f"{ref_id}: 1.0 mutation must remain false")
        require(set(item["activation"]) == candidate_ids, f"{ref_id}: activation mapping incomplete")
        source = ROOT / item["source_fixture"]
        require(source.exists(), f"{ref_id}: source fixture missing")
    messages.append("1.0 reference regression mapping: complete")

    return messages


def main() -> int:
    try:
        messages = validate()
    except (ValidationError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f"EAIMS 1.1 draft validation FAILED: {exc}", file=sys.stderr)
        return 1

    print("EAIMS 1.1 draft validation PASS")
    for message in messages:
        print(f"- {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
