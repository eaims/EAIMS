from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "FINAL-READINESS-v1.1-DRAFT.md"

def test_v11_readiness_is_not_misrepresented_as_release_ready():
    text = READINESS.read_text(encoding="utf-8")
    assert "NOT READY FOR NORMATIVE FREEZE" in text
    assert "Latest full CI run passes" in text
    assert "inter-rater" in text.lower()
    assert "ADV-004, ADV-006, ADV-009" in text
