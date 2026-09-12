from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "FINAL-READINESS-v1.1-DRAFT.md"

def test_v11_readiness_is_not_misrepresented_as_normatively_frozen():
    text = READINESS.read_text(encoding="utf-8")
    assert "CANDIDATE-FREEZE REVIEW READY — NOT NORMATIVELY FROZEN" in text
    assert "At least two independent assessor passes" in text
    assert "inter-rater" in text.lower()
    assert "ADV-004, ADV-006, ADV-009" in text
