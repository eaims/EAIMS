from pathlib import Path
import json
import pytest
import yaml
from src.eaims.engine import assess_fixture, validate_fixture, validate_evidence
from src.eaims.cli import main

ROOT = Path(__file__).resolve().parents[1]


def fixture():
    return yaml.safe_load((ROOT / 'reference-implementations/ri-02-enterprise-service-agent/input/fixture.yaml').read_text())


@pytest.mark.parametrize('value', ['', None, ' ', False, 0, '2026-09-09T00:00:00'])
def test_evidence_requires_timezone_aware_collection_time(value):
    f = fixture()
    f['evidence'][0]['collected_at'] = value
    assert 'invalid:collected_at' in validate_evidence(f['evidence'][0])
    assert validate_fixture(f)
    with pytest.raises(ValueError):
        assess_fixture(f)


@pytest.mark.parametrize('path,value', [
    (('capabilities', 0, 'anchor_observed', 'L4'), 'false'),
    (('capabilities', 0, 'operating_cycles'), -1),
    (('capabilities', 0, 'adaptation_cycles'), 1.5),
    (('capabilities', 0, 'capability_id'), []),
    (('evidence', 0, 'evidence_id'), {}),
    (('evidence', 0, 'source'), None),
    (('requirement_results', 0, 'evidence_refs'), 'EV-1'),
    (('system', 'agentic'), 'false'),
    (('permission_envelope', 'delegation_allowed'), 'false'),
    (('permission_envelope', 'financial_limit'), float('nan')),
    (('permission_envelope', 'financial_limit'), float('inf')),
    (('permission_envelope', 'financial_limit'), -1),
    (('permission_envelope', 'financial_limit'), True),
    (('gate_inputs',), ['PASS']),
    (('gate_inputs', 'G3-01'), 1),
    (('gate_inputs', 'G3-01'), {}),
    (('agent_events',), [None]),
    (('agent_events', 0, 'occurred_at'), ''),
    (('agent_events', 0, 'financial_amount'), '100'),
    (('risk_profile', 'impact'), []),
])
def test_invalid_types_rejected_before_scoring(path, value):
    f = fixture()
    node = f
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value
    assert validate_fixture(f)
    with pytest.raises(ValueError, match='Invalid EAIMS fixture'):
        assess_fixture(f)


def test_future_evidence_rejected_across_timezone_offsets():
    f = fixture()
    f['evidence'][0]['collected_at'] = '2026-09-10T04:00:00+03:30'
    assert any('after_cutoff' in error for error in validate_fixture(f))


def test_cyclic_yaml_and_non_string_keys_rejected():
    f = fixture()
    f['extension'] = f
    assert any('recursive data' in e for e in validate_fixture(f))
    f = fixture()
    f['extension'] = {1: 'value'}
    assert any('keys must be strings' in e for e in validate_fixture(f))


def test_cli_invalid_input_reports_error_without_traceback(tmp_path, capsys):
    f = fixture()
    f['gate_inputs'] = [True]
    path = tmp_path / 'bad.yaml'
    path.write_text(yaml.safe_dump(f))
    assert main(['assess', str(path), '--out', str(tmp_path / 'out')]) == 1
    captured = capsys.readouterr()
    assert 'gate_inputs' in captured.err
    assert 'Traceback' not in captured.err
    assert not (tmp_path / 'out').exists()


def test_cli_rejects_duplicate_yaml_keys(tmp_path, capsys):
    path = tmp_path / 'duplicate.yaml'
    path.write_text('reviews: []\nreviews: []\n')
    assert main(['review', 'summarize', str(path)]) == 2
    assert 'duplicate mapping key' in capsys.readouterr().err


def test_reference_results_conform_to_v1_output_schema():
    from jsonschema import Draft202012Validator, FormatChecker
    schema = json.loads((ROOT / 'schemas/assessment-result-v1.schema.json').read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for path in (ROOT / 'reference-implementations').glob('*/expected/result.json'):
        result = json.loads(path.read_text())
        assert not list(validator.iter_errors(result))
        if result['assessment_type'] == 'TARGETED':
            result['enterprise_index'] = 3
            assert list(validator.iter_errors(result))


def test_non_json_context_rejected_before_result_hashing():
    f = fixture()
    f['system']['extension'] = {1, 2}
    assert any('JSON-compatible' in e for e in validate_fixture(f))
