from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "spec" / "adversarial-agentic-package-1.1-draft.yaml"


def _collect_paths(node):
    if isinstance(node, str):
        if "/" in node or node.endswith(".md") or node.endswith(".yaml") or node.endswith(".py"):
            return [node]
        return []
    if isinstance(node, list):
        result = []
        for item in node:
            result.extend(_collect_paths(item))
        return result
    if isinstance(node, dict):
        result = []
        for value in node.values():
            result.extend(_collect_paths(value))
        return result
    return []


def test_v11_package_manifest_paths_exist():
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert data["normative"] is False
    paths = _collect_paths({
        k: v for k, v in data.items()
        if k not in {"profile_id", "status", "normative", "target_version", "package_rules"}
    })
    missing = [p for p in paths if not (ROOT / p).exists()]
    assert not missing, f"missing manifest paths: {missing}"


def test_v11_package_manifest_includes_critical_i4_and_validator():
    text = MANIFEST.read_text(encoding="utf-8")
    assert "validation/CRITICAL-I4-CASE-1.1-DRAFT.md" in text
    assert "tools/validate_v11_draft.py" in text
