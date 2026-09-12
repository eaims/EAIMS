from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "spec" / "adversarial-agentic-1.1-draft.yaml"
ANCHORS = ROOT / "spec" / "adversarial-agentic-anchors-1.1-draft.yaml"
POSITIVE = ROOT / "validation" / "v11-adversarial-positive.yaml"
NEGATIVE = ROOT / "validation" / "v11-adversarial-negative.yaml"


def _load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_v11_anchor_overlay_references_only_candidate_requirements():
    profile = _load(PROFILE)
    anchors = _load(ANCHORS)
    known = {r["requirement_id"] for r in profile["candidate_requirements"]}
    referenced = {
        req
        for capability in anchors["capability_extensions"].values()
        for req in capability["requirement_minimum_levels"]
    }
    assert referenced == known


def test_v11_anchor_levels_are_valid():
    anchors = _load(ANCHORS)
    allowed = {"L1", "L2", "L3", "L4", "L5"}
    for capability in anchors["capability_extensions"].values():
        assert set(capability["requirement_minimum_levels"].values()).issubset(allowed)


def test_v11_positive_fixture_satisfies_all_applicable_candidate_requirements():
    profile = _load(PROFILE)
    fixture = _load(POSITIVE)
    applicable_ids = {
        r["requirement_id"] for r in profile["candidate_requirements"]
        if r["requirement_id"] != "EAIMS-ADV-010"
    }
    assert fixture["expected_outcome"] == "PASS"
    assert all(fixture["requirements"][rid]["result"] == "SATISFIED" for rid in applicable_ids)
    assert fixture["requirements"]["EAIMS-ADV-010"]["result"] == "NOT_APPLICABLE"
    assert all(v == "PASS" for v in fixture["expected_gate_extensions"].values())


def test_v11_negative_fixture_exercises_each_g3_extension_failure_path():
    fixture = _load(NEGATIVE)
    assert fixture["expected_outcome"] == "BREACH"
    expected = fixture["expected_gate_extensions"]
    assert set(expected) == {"G3-13", "G3-14", "G3-15", "G3-16", "G3-17"}
    assert any(v == "BREACH" for v in expected.values())
    assert "INCOMPLETE" in expected.values()


def test_v11_fixture_requirement_ids_are_known():
    profile = _load(PROFILE)
    known = {r["requirement_id"] for r in profile["candidate_requirements"]}
    for path in (POSITIVE, NEGATIVE):
        fixture = _load(path)
        assert set(fixture["requirements"]) == known
