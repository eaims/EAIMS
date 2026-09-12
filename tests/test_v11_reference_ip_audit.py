from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "tools" / "audit_v11_reference_ip.py"


def test_v11_reference_ip_hygiene_audit_passes():
    spec = importlib.util.spec_from_file_location("audit_v11_reference_ip", AUDIT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    messages = module.audit()
    assert "endorsement/equivalence claims: PASS" in messages
    assert "reference-boundary language: PASS" in messages
