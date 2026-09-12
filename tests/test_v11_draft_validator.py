from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_v11_draft.py"
CRITICAL = ROOT / "validation" / "CRITICAL-I4-CASE-1.1-DRAFT.md"


def _module():
    spec = importlib.util.spec_from_file_location("validate_v11_draft", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_v11_draft_validator_passes_repository_package():
    module = _module()
    messages = module.validate()
    assert "anchor coverage: complete" in messages
    assert "activation coverage: complete" in messages
    assert "gate references/effects: complete" in messages
    assert "1.0 reference regression mapping: complete" in messages


def test_v11_critical_i4_case_exercises_deployment_blocks_and_strictest_cap():
    text = CRITICAL.read_text(encoding="utf-8")
    assert "I4 / A4 / R4 / S4 / D3" in text
    assert "process termination without credential/tool authority revocation is not containment" in text.lower()
    assert "strictest maturity cap prevails: **L2**" in text
    assert "deployment_block" in text
    assert "scale_block" in text
