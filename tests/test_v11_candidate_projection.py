from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "spec" / "adversarial-agentic-normative-candidate-1.1.yaml"
PROJECTION = ROOT / "spec" / "adversarial-agentic-candidate-projection-1.1.yaml"

def test_candidate_projection_matches_candidate_requirement_set():
    candidate = yaml.safe_load(CANDIDATE.read_text(encoding="utf-8"))
    projection = yaml.safe_load(PROJECTION.read_text(encoding="utf-8"))
    candidate_ids = {r["requirement_id"] for r in candidate["new_requirements"]}
    assert set(projection["new_requirement_ids"]) == candidate_ids
    assert set(projection["amended_existing_requirement_ids"]) == set(candidate["amended_existing_requirements"])

def test_candidate_projection_excludes_adv009_from_active_candidate_semantics():
    projection = yaml.safe_load(PROJECTION.read_text(encoding="utf-8"))
    active = set(projection["activation_projection"])
    evidence = set(projection["evidence_projection"])
    gates = {rid for ids in projection["gate_projection"].values() for rid in ids}
    assert "EAIMS-ADV-009" not in active
    assert "EAIMS-ADV-009" not in evidence
    assert "EAIMS-ADV-009" not in gates
    assert projection["development_only_ids"] == ["EAIMS-ADV-009"]

def test_candidate_projection_includes_strengthened_msp_semantics():
    projection = yaml.safe_load(PROJECTION.read_text(encoding="utf-8"))
    assert "EAIMS-MSP-005" in projection["activation_projection"]
    assert "EAIMS-MSP-008" in projection["activation_projection"]
    assert "concentration-risk analysis" in projection["evidence_projection"]["EAIMS-MSP-005"]
    assert "dependency graph" in projection["evidence_projection"]["EAIMS-MSP-008"]
