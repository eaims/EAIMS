from copy import deepcopy
from pathlib import Path
import json
import pytest
import yaml
from src.eaims.cli import main
from src.eaims.review import aggregate_findings, apply_resolutions

ROOT = Path(__file__).resolve().parents[1]


def fixture():
    return yaml.safe_load((ROOT / 'validation/review-workflow-fixture.yaml').read_text())


def test_duplicate_review_id_rejected():
    data = fixture()
    records = data['reviews']
    with pytest.raises(ValueError, match='Duplicate review_id'):
        aggregate_findings(records + deepcopy(records))


def test_duplicate_finding_cannot_overwrite_blocker():
    record = fixture()['reviews'][0]
    record['findings'][0]['severity'] = 'BLOCKER'
    duplicate = deepcopy(record['findings'][0])
    duplicate['severity'] = 'MINOR'
    record['findings'].append(duplicate)
    with pytest.raises(ValueError, match='Duplicate finding_key'):
        aggregate_findings([record])


def test_duplicate_ledger_key_rejected_even_without_resolutions():
    ledger = [{'finding_key': 'R:F', 'severity': 'BLOCKER'}, {'finding_key': 'R:F', 'severity': 'MINOR'}]
    with pytest.raises(ValueError, match='Duplicate finding_key'):
        apply_resolutions(ledger, [])


def test_applying_resolution_preserves_original_ledger():
    data = fixture()
    ledger = aggregate_findings(data['reviews'])
    original = deepcopy(ledger)
    updated = apply_resolutions(ledger, data['resolutions'])
    assert ledger == original
    assert updated[0]['resolution_status'] == 'RESOLVED'


@pytest.mark.parametrize('unmet,strict,expected', [(True, False, 0), (True, True, 1), (False, True, 0)])
def test_cli_review_exit_code_and_reports(tmp_path, unmet, strict, expected):
    data = fixture()
    if unmet:
        data['resolutions'] = []
    path = tmp_path / 'review.yaml'
    path.write_text(yaml.safe_dump(data))
    out = tmp_path / 'reports'
    args = ['review', 'summarize', str(path), '--out', str(out)]
    if strict:
        args.append('--fail-on-unmet')
    assert main(args) == expected
    summary = json.loads((out / 'review-summary.json').read_text())
    assert summary['rc_gate']['review_completed_for_rc'] is (not unmet)
    assert (out / 'findings-ledger.json').exists()
    assert (out / 'review-summary.md').exists()


@pytest.mark.parametrize('data', [None, [], {'reviews': {}}, {'resolutions': {}}])
def test_cli_malformed_review_structure(tmp_path, data):
    path = tmp_path / 'review.yaml'
    path.write_text(yaml.safe_dump(data))
    assert main(['review', 'summarize', str(path), '--out', str(tmp_path / 'out')]) == 2
