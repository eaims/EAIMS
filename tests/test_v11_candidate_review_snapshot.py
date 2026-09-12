from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SNAPSHOT=ROOT/"review"/"CANDIDATE-REVIEW-SNAPSHOT-1.1-DRAFT.md"

def test_candidate_review_snapshot_pins_green_head_and_ci():
    text=SNAPSHOT.read_text(encoding="utf-8")
    assert "9f7e4bc9f2658d72ba73ee3b7d05957c89af8609" in text
    assert "EAIMS Validation #265" in text
    assert "CI status: PASS" in text
    assert "fb21bc6f65647bd7f15caca61229fd5da48f5246" in text
    assert "superseded" in text.lower()
    assert "responses from different SHAs must not be compared" in text
