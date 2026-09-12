from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSESSOR = ROOT / "docs" / "ASSESSOR-PROTOCOL-ADVERSARIAL-1.1-DRAFT.md"
TI = ROOT / "docs" / "THREAT-INTELLIGENCE-PROTOCOL-1.1-DRAFT.md"

def test_v11_assessor_protocol_covers_all_adv_requirements():
    text = ASSESSOR.read_text(encoding="utf-8")
    for i in range(1, 11):
        assert f"ADV-{i:03d}" in text

def test_v11_assessor_protocol_forbids_na_from_missing_context():
    text = ASSESSOR.read_text(encoding="utf-8")
    assert "infer NOT_APPLICABLE from missing context" in text

def test_v11_threat_intelligence_protocol_is_closed_loop():
    text = TI.read_text(encoding="utf-8")
    assert "Source -> Triage -> Exposure mapping -> Decision -> Action -> Verification -> Learning" in text
    for state in ("ACTION_REQUIRED", "MONITOR", "ACCEPTED", "NOT_APPLICABLE", "NEEDS_ANALYSIS", "SUPERSEDED"):
        assert state in text
