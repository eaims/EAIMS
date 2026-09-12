from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "spec" / "adversarial-agentic-1.1-draft.yaml"
BASE_REQUIREMENTS = ROOT / "spec" / "requirements.yaml"


def _load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_v11_adversarial_profile_is_explicitly_non_normative():
    data = _load(PROFILE)
    assert data["status"] == "development_draft"
    assert data["normative"] is False
    assert data["target_version"] == 1.1


def test_v11_candidate_requirement_ids_are_unique_and_do_not_collide_with_v1():
    profile = _load(PROFILE)
    base = _load(BASE_REQUIREMENTS)

    candidate_ids = [item["requirement_id"] for item in profile["candidate_requirements"]]
    assert len(candidate_ids) == len(set(candidate_ids))

    base_requirements = base.get("requirements", base)
    base_ids = {item["requirement_id"] for item in base_requirements}
    assert set(candidate_ids).isdisjoint(base_ids)


def test_v11_gate_extensions_reference_known_candidate_requirements():
    profile = _load(PROFILE)
    candidate_ids = {item["requirement_id"] for item in profile["candidate_requirements"]}

    gate_ids = []
    for family in profile["candidate_gate_extensions"].values():
        for gate in family["add_checks"]:
            gate_ids.append(gate["gate_id"])
            assert set(gate["requirement_ids"]).issubset(candidate_ids)

    assert len(gate_ids) == len(set(gate_ids))


def test_v11_candidate_requirements_have_required_assessment_metadata():
    profile = _load(PROFILE)
    allowed_mv = {"MV1", "MV2", "MV3", "MV4"}
    allowed_normative = {"SHALL", "SHALL_NOT", "SHOULD", "SHOULD_NOT", "MAY"}

    for item in profile["candidate_requirements"]:
        assert item["capability_id"]
        assert item["title"]
        assert item["statement"]
        assert item["activation"]
        assert item["machine_verifiability"] in allowed_mv
        assert item["normative_level"] in allowed_normative
