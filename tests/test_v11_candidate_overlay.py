from pathlib import Path
import importlib.util
import yaml

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "spec" / "adversarial-agentic-normative-candidate-1.1.yaml"
DECISION = ROOT / "docs" / "FINAL-CONSOLIDATION-DECISION-1.1-DRAFT.md"
AUDIT = ROOT / "tools" / "audit_v11_candidate.py"

def test_candidate_overlay_has_nine_new_requirements_and_two_amendments():
    data = yaml.safe_load(CANDIDATE.read_text(encoding="utf-8"))
    assert data["normative"] is False
    assert len(data["new_requirements"]) == 9
    assert set(data["amended_existing_requirements"]) == {"EAIMS-MSP-005","EAIMS-MSP-008"}
    assert "EAIMS-ADV-009" not in {r["requirement_id"] for r in data["new_requirements"]}

def test_final_consolidation_decision_is_explicit():
    text = DECISION.read_text(encoding="utf-8")
    assert "ADV-004 — KEEP" in text
    assert "ADV-006 — KEEP" in text
    assert "ADV-009 — MERGE INTO MSP-005 / MSP-008" in text

def test_candidate_audit_module_runs_and_passes():
    spec = importlib.util.spec_from_file_location("audit_v11_candidate", AUDIT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    assert module.main() == 0
