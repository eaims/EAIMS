from pathlib import Path
import hashlib
import yaml

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "spec" / "adversarial-agentic-1.1-draft.yaml"
ACTIVATION = ROOT / "spec" / "adversarial-agentic-activation-1.1-draft.yaml"
REGRESSION = ROOT / "validation" / "v11-reference-regression.yaml"


def _load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_activation_rules_cover_every_candidate_requirement_exactly_once():
    profile = _load(PROFILE)
    activation = _load(ACTIVATION)
    candidate_ids = {r["requirement_id"] for r in profile["candidate_requirements"]}
    assert set(activation["rules"]) == candidate_ids


def test_activation_defaults_use_defined_applicability_states():
    activation = _load(ACTIVATION)
    allowed = {"APPLICABLE", "NOT_APPLICABLE", "CONDITIONALLY_APPLICABLE", "NOT_ASSESSED"}
    for rule in activation["rules"].values():
        assert rule["default"] in allowed
        if "fallback" in rule:
            assert rule["fallback"] in allowed


def test_reference_regression_covers_all_candidates_for_all_reference_implementations():
    profile = _load(PROFILE)
    regression = _load(REGRESSION)
    candidate_ids = {r["requirement_id"] for r in profile["candidate_requirements"]}
    assert set(regression["reference_implementations"]) == {"RI-01", "RI-02", "RI-03"}
    for item in regression["reference_implementations"].values():
        assert set(item["activation"]) == candidate_ids
        assert item["expected_1_0_mutation"] is False


def test_reference_fixtures_remain_untouched_by_v11_overlay_design():
    regression = _load(REGRESSION)
    expected_paths = {
        "RI-01": ROOT / "reference-implementations" / "ri-01-api-consumed-analytics" / "input" / "fixture.yaml",
        "RI-02": ROOT / "reference-implementations" / "ri-02-enterprise-service-agent" / "input" / "fixture.yaml",
        "RI-03": ROOT / "reference-implementations" / "ri-03-high-impact-decision-support" / "input" / "fixture.yaml",
    }
    for key, path in expected_paths.items():
        assert regression["reference_implementations"][key]["source_fixture"] == str(path.relative_to(ROOT))
        assert _sha(path)


def test_non_applicable_cannot_be_inferred_from_missing_context():
    activation = _load(ACTIVATION)
    rules = activation["decision_rules"]
    assert any("Missing activation evidence" in x for x in rules)
    assert any("NOT_APPLICABLE requires" in x for x in rules)
