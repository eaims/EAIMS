from pathlib import Path
import yaml
from src.eaims.review import validate_review_record, aggregate_findings, apply_resolutions, rc_review_gate, review_summary, render_review_markdown

ROOT = Path(__file__).resolve().parents[1]


def _fixture():
    return yaml.safe_load((ROOT / "validation/review-workflow-fixture.yaml").read_text())


def test_review_record_validates_against_schema():
    data = _fixture()
    assert validate_review_record(data["reviews"][0], ROOT) == []


def test_finding_ledger_and_resolution_preserve_review_identity():
    data = _fixture()
    ledger = aggregate_findings(data["reviews"])
    assert ledger[0]["finding_key"] == "REVIEW-DEMO:F-001"
    out = apply_resolutions(ledger, data["resolutions"])
    assert out[0]["resolution_status"] == "RESOLVED"
    assert out[0]["review_id"] == "REVIEW-DEMO"


def test_rc_gate_requires_resolved_blocker_and_major_findings():
    data = _fixture()
    ledger = aggregate_findings(data["reviews"])
    before = rc_review_gate(data["reviews"], ledger)
    assert before["review_completed_for_rc"] is False
    ledger = apply_resolutions(ledger, data["resolutions"])
    after = rc_review_gate(data["reviews"], ledger)
    assert after["review_completed_for_rc"] is True


def test_not_ready_or_rereview_disposition_blocks_exit():
    data = _fixture()
    ledger = apply_resolutions(aggregate_findings(data["reviews"]), data["resolutions"])
    record = dict(data["reviews"][0])
    record["overall_decision"] = "NOT_READY_FOR_RC"
    assert rc_review_gate([record], ledger)["review_completed_for_rc"] is False
    record["overall_decision"] = "REVISE_AND_REREVIEW"
    assert rc_review_gate([record], ledger)["review_completed_for_rc"] is False


def test_review_summary_is_human_readable_and_keeps_claim_boundary():
    data = _fixture()
    ledger = apply_resolutions(aggregate_findings(data["reviews"]), data["resolutions"])
    summary = review_summary(data["reviews"], ledger)
    md = render_review_markdown(summary, ledger)
    assert "RC_REVIEW_EXIT_CRITERIA_MET" in md
    assert "empirical validity" in md

def test_resolution_schema_validation_rejects_missing_fields():
    from src.eaims.review import validate_resolution_record
    errs=validate_resolution_record({'resolution_id':'R'})
    assert errs


def test_duplicate_resolution_for_same_finding_rejected():
    from copy import deepcopy
    from src.eaims.review import aggregate_findings, apply_resolutions
    data=_fixture()
    ledger=aggregate_findings(data['reviews'])
    r1=deepcopy(data['resolutions'][0])
    r2=deepcopy(r1); r2['resolution_id']='RES-DEMO-002'
    import pytest
    with pytest.raises(ValueError):
        apply_resolutions(ledger,[r1,r2])
