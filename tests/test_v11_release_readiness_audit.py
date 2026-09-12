from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "tools" / "audit_v11_release_readiness.py"
CRITERIA = ROOT / "review" / "RELEASE-READINESS-AUDIT-1.1-DRAFT.md"


def _module():
    spec = importlib.util.spec_from_file_location("audit_v11_release_readiness", AUDIT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_v11_release_readiness_audit_passes_current_candidate_package():
    module = _module()
    messages = module.audit()
    assert "version/non-normative hygiene: PASS" in messages
    assert "requirement IDs/capabilities: PASS" in messages
    assert "candidate gate references: PASS" in messages
    assert "canonical 1.0 baseline preservation: PASS" in messages


def test_v11_release_readiness_criteria_define_freeze_blockers():
    text = CRITERIA.read_text(encoding="utf-8")
    assert "Freeze blockers" in text
    assert "failing CI" in text
    assert "orphan or colliding IDs" in text
    assert "external-framework language that creates IP/equivalence risk" in text
