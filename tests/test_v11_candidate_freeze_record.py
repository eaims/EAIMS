from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "review" / "CANDIDATE-FREEZE-DECISION-1.1-DRAFT.md"

def test_candidate_freeze_record_preserves_human_review_blockers():
    text = RECORD.read_text(encoding="utf-8")
    assert "CANDIDATE-FREEZE REVIEW READY" in text
    assert "At least two independent assessor passes" in text
    assert "A green CI result alone does not authorize" in text
    assert "changing `normative: false` to true" in text
    assert "This does **not** constitute normative freeze." in text
