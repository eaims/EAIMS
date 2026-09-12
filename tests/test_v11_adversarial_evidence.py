from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "spec" / "adversarial-agentic-1.1-draft.yaml"
EVIDENCE = ROOT / "spec" / "adversarial-agentic-evidence-1.1-draft.yaml"

def _load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def test_v11_evidence_overlay_covers_every_candidate_requirement():
    profile = _load(PROFILE)
    evidence = _load(EVIDENCE)
    ids = {r["requirement_id"] for r in profile["candidate_requirements"]}
    assert set(evidence["requirements"]) == ids

def test_v11_evidence_overlay_contains_supporting_and_counter_evidence():
    evidence = _load(EVIDENCE)
    for item in evidence["requirements"].values():
        assert item["supporting"]
        assert item["counter"]
        assert item["preferred_class"] in {"E1","E2","E3","E4"}

def test_v11_high_maturity_evidence_rejects_policy_only_inflation():
    evidence = _load(EVIDENCE)
    rules = " ".join(evidence["high_maturity_rules"])
    assert "Policy-only evidence is insufficient" in rules
    assert "Counter-evidence must be preserved" in rules
