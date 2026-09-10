from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_review_protocol_has_required_domains_and_exit_rule():
    p = yaml.safe_load((ROOT / "spec/review-protocol.yaml").read_text())
    ids = {x["id"] for x in p["review_domains"]}
    assert ids == {"ARCH", "MAT", "EVD", "GOV", "RSK", "EXE", "ENT", "RES"}
    assert "BLOCKER" in p["severity_levels"]
    assert "MAJOR" in p["resolution_required_for"]
    assert "empirical" in p["claim_boundary"].lower()


def test_feedback_template_declares_independent_review_and_limitations():
    f = yaml.safe_load((ROOT / "review/FEEDBACK-TEMPLATE.yaml").read_text())
    assert f["independence_class"] in {"EXTERNAL_INDEPENDENT", "INTERNAL_INDEPENDENT"}
    assert f["limitations_acknowledged"] is True
    assert f["domains_reviewed"]
    assert f["findings"]


def test_review_feedback_schema_and_readiness_manifest_parse():
    schema = json.loads((ROOT / "schemas/review-feedback.schema.json").read_text())
    ready = json.loads((ROOT / "validation/rc-review-readiness.json").read_text())
    assert schema["title"] == "EAIMS RC Review Feedback"
    assert ready["independent_review_completed"] is False
    assert ready["rc_review_status"] == "READY_TO_REQUEST_REVIEW_NOT_COMPLETED"


def test_review_package_has_no_endorsement_or_empirical_validation_claim():
    text = "\n".join(p.read_text() for p in (ROOT / "review").glob("*.md"))
    low = text.lower()
    assert "not a request to certify" in low or "not** a request to certify" in low
    assert "not" in low and "empirical" in low
