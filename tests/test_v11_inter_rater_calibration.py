from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKSHEET = ROOT / "review" / "INDEPENDENT-ASSESSOR-CALIBRATION-1.1-DRAFT.md"
SCHEMA = ROOT / "review" / "inter-rater-comparison-1.1-draft.yaml"

def test_inter_rater_calibration_requires_independent_completion():
    text = WORKSHEET.read_text(encoding="utf-8")
    assert "complete the worksheet independently" in text
    assert "Do not infer NOT_APPLICABLE from missing evidence." in text
    for case in ("IR-01","IR-02","IR-03","IR-04","IR-05","IR-06","IR-07"):
        assert case in text

def test_inter_rater_comparison_policy_blocks_unresolved_critical_ambiguity():
    data = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    assert data["comparison_policy"]["unresolved_critical_semantic_disagreement_blocks_freeze"] is True
    assert set(data["comparison_policy"]["exact_agreement_fields"]) == {"applicability","result","gate_result"}
