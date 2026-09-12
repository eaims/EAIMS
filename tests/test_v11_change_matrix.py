from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "spec" / "adversarial-agentic-1.1-draft.yaml"
MATRIX = ROOT / "docs" / "REQUIREMENT-CHANGE-MATRIX-1.1-DRAFT.md"


def test_v11_change_matrix_mentions_every_candidate_requirement():
    profile = yaml.safe_load(PROFILE.read_text(encoding="utf-8"))
    text = MATRIX.read_text(encoding="utf-8")
    candidate_ids = {r["requirement_id"] for r in profile["candidate_requirements"]}
    mentioned = set(re.findall(r"EAIMS-ADV-\d{3}", text))
    assert candidate_ids.issubset(mentioned)


def test_v11_change_matrix_declares_backward_compatibility_test():
    text = MATRIX.read_text(encoding="utf-8")
    assert "historical 1.0.x results remain interpretable" in text
    assert "No consolidation should occur before worked-case and inter-rater validation." in text
