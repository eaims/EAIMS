from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
EFFECTS = ROOT / "spec" / "adversarial-agentic-gate-effects-1.1-draft.yaml"
CONSOLIDATION = ROOT / "docs" / "REQUIREMENT-CONSOLIDATION-1.1-DRAFT.md"
INTERRATER = ROOT / "validation" / "INTER-RATER-CASES-1.1-DRAFT.md"

def test_v11_gate_effects_cover_all_candidate_g3_extensions():
    data = yaml.safe_load(EFFECTS.read_text(encoding="utf-8"))
    assert set(data["gate_effects"]) == {"G3-13","G3-14","G3-15","G3-16","G3-17"}

def test_v11_gate_effects_use_supported_consequences():
    data = yaml.safe_load(EFFECTS.read_text(encoding="utf-8"))
    allowed = {"critical_risk_flag","maturity_cap","scale_block","deployment_block","mandatory_remediation","reassessment_required"}
    for gate in data["gate_effects"].values():
        assert set(gate["on_breach"]).issubset(allowed)
        if "maturity_cap" in gate:
            assert gate["maturity_cap"] in {"L1","L2","L3","L4","L5"}

def test_v11_consolidation_record_covers_all_candidates():
    text = CONSOLIDATION.read_text(encoding="utf-8")
    for i in range(1, 11):
        assert f"ADV-{i:03d}" in text
    assert "MERGE CANDIDATE" in text

def test_v11_interrater_cases_include_core_ambiguities():
    text = INTERRATER.read_text(encoding="utf-8")
    for case in ("IR-01","IR-02","IR-03","IR-04","IR-05","IR-06","IR-07"):
        assert case in text
    assert "process termination is not equivalent to containment of authority" in text
    assert "must not be marked NOT_APPLICABLE solely because evidence is absent" in text
