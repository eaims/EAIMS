from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SNAPSHOT=ROOT/"review"/"CANDIDATE-REVIEW-SNAPSHOT-1.1-DRAFT.md"

def test_candidate_review_snapshot_pins_green_head_and_ci():
    text=SNAPSHOT.read_text(encoding="utf-8")
    assert "fb21bc6f65647bd7f15caca61229fd5da48f5246" in text
    assert "EAIMS Validation #248" in text
    assert "CI status: PASS" in text
    assert "responses from different SHAs must not be compared" in text
