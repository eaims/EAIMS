from pathlib import Path
import json
from src.eaims.cli import main

ROOT = Path(__file__).resolve().parents[1]

REFERENCE_IMPLEMENTATIONS = (
    "ri-01-api-consumed-analytics",
    "ri-02-enterprise-service-agent",
    "ri-03-high-impact-decision-support",
)


def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _normalized_text(path):
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip() + "\n"


def test_v11_overlay_does_not_change_recomputed_v1_reference_outputs(tmp_path):
    for name in REFERENCE_IMPLEMENTATIONS:
        root = ROOT / "reference-implementations" / name
        fixture = root / "input" / "fixture.yaml"
        expected = root / "expected"
        out = tmp_path / name

        assert main(["assess", str(fixture), "--out", str(out)]) == 0

        actual_result = _json(out / "result.json")
        expected_result = _json(expected / "result.json")
        assert actual_result == expected_result, (
            f"{name}: recomputed result.json differs semantically from frozen 1.0 expected output"
        )
        assert actual_result.get("result_hash") == expected_result.get("result_hash"), (
            f"{name}: deterministic result_hash changed"
        )

        assert _normalized_text(out / "report.md") == _normalized_text(expected / "report.md"), (
            f"{name}: recomputed report.md differs from frozen 1.0 expected output"
        )
