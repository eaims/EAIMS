from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "review" / "review-findings-log-1.1-draft.yaml"

def test_review_findings_log_preserves_resolution_history_rules():
    data = yaml.safe_load(LOG.read_text(encoding="utf-8"))
    assert data["findings"] == []
    rules = " ".join(data["rules"])
    assert "must not be deleted" in rules
    assert "critical finding remains OPEN" in rules
    assert "Rejected findings require retained rationale." in rules
