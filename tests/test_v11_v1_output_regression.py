from pathlib import Path
from src.eaims.cli import main

ROOT = Path(__file__).resolve().parents[1]

REFERENCE_IMPLEMENTATIONS = (
    "ri-01-api-consumed-analytics",
    "ri-02-enterprise-service-agent",
    "ri-03-high-impact-decision-support",
)


def test_v11_overlay_does_not_change_recomputed_v1_reference_outputs(tmp_path):
    for name in REFERENCE_IMPLEMENTATIONS:
        root = ROOT / "reference-implementations" / name
        fixture = root / "input" / "fixture.yaml"
        expected = root / "expected"
        out = tmp_path / name

        assert main(["assess", str(fixture), "--out", str(out)]) == 0

        assert (out / "result.json").read_bytes() == (expected / "result.json").read_bytes(), (
            f"{name}: recomputed result.json differs from frozen 1.0 expected output"
        )
        assert (out / "report.md").read_bytes() == (expected / "report.md").read_bytes(), (
            f"{name}: recomputed report.md differs from frozen 1.0 expected output"
        )
