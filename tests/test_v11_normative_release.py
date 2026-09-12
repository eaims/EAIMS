from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "spec" / "adversarial-agentic-1.1.yaml"
NOTES = ROOT / "RELEASE-NOTES-v1.1.0.md"
FREEZE = ROOT / "review" / "NORMATIVE-FREEZE-DECISION-1.1.0.md"


def test_v11_release_overlay_is_normative_and_final():
    data = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    assert data["profile_id"] == "EAIMS-1.1-NORMATIVE-OVERLAY"
    assert data["status"] == "normative_release"
    assert data["normative"] is True
    assert data["target_version"] == 1.1
    assert len(data["new_requirements"]) == 9
    assert set(data["amended_existing_requirements"]) == {"EAIMS-MSP-005", "EAIMS-MSP-008"}
    assert "EAIMS-ADV-009" not in {r["requirement_id"] for r in data["new_requirements"]}


def test_v11_release_discloses_validation_boundary():
    notes = NOTES.read_text(encoding="utf-8").lower()
    freeze = FREEZE.read_text(encoding="utf-8").lower()
    assert "maintainer-frozen" in notes
    assert "does not claim independent third-party assessor validation" in notes
    assert "independent assessor calibration is not a release prerequisite" in freeze
    assert "no claim of independent third-party validation is made" in freeze
