from pathlib import Path
import yaml
import pytest
from src.eaims.verification import evaluate_rule, mutate_to_fail, verify_critical_machine_requirements
from src.eaims.assessor import protocol_index, validate_assessor_record, normalize_assessor_result

ROOT=Path(__file__).resolve().parents[1]
RULES=yaml.safe_load((ROOT/'spec/machine-verification.yaml').read_text())['rules']
POS=yaml.safe_load((ROOT/'validation/critical-machine-verification-positive.yaml').read_text())


def test_machine_verification_covers_all_critical_mv1_mv2_requirements():
    reqs=yaml.safe_load((ROOT/'spec/requirements.yaml').read_text())['requirements']
    expected={r['requirement_id'] for r in reqs if r['criticality']=='critical' and r['normative_level'] in ('SHALL','SHALL_NOT') and r['machine_verifiability'] in ('MV1','MV2')}
    actual={r['requirement_id'] for r in RULES}
    assert actual==expected

@pytest.mark.parametrize('rule',RULES,ids=lambda r:r['requirement_id'])
def test_each_critical_machine_rule_positive(rule):
    assert evaluate_rule(rule,POS)['result']=='SATISFIED'

@pytest.mark.parametrize('rule',RULES,ids=lambda r:r['requirement_id'])
def test_each_critical_machine_rule_negative(rule):
    bad=mutate_to_fail(rule,POS)
    assert evaluate_rule(rule,bad)['result']=='NOT_SATISFIED'


def test_batch_verifier_returns_all_rules():
    out=verify_critical_machine_requirements(POS)
    assert len(out)==len(RULES)==33
    assert all(x['result']=='SATISFIED' for x in out)


def test_assessor_protocol_covers_all_critical_mv3_mv4_requirements():
    reqs=yaml.safe_load((ROOT/'spec/requirements.yaml').read_text())['requirements']
    expected={r['requirement_id'] for r in reqs if r['criticality']=='critical' and r['normative_level'] in ('SHALL','SHALL_NOT') and r['machine_verifiability'] in ('MV3','MV4')}
    assert set(protocol_index())==expected


def test_valid_assessor_record_normalizes():
    rec=yaml.safe_load((ROOT/'validation/assessor-record-example.yaml').read_text())
    assert validate_assessor_record(rec)==[]
    assert normalize_assessor_result(rec)['result']=='SATISFIED'


def test_assessor_record_requires_rationale_and_evidence():
    rec=yaml.safe_load((ROOT/'validation/assessor-record-example.yaml').read_text())
    rec['rationale']=''; rec['evidence_refs']=[]
    errs=validate_assessor_record(rec)
    assert 'missing:rationale' in errs and 'missing:evidence_refs' in errs


def test_not_applicable_requires_applicability_rationale():
    rec=yaml.safe_load((ROOT/'validation/assessor-record-example.yaml').read_text())
    rec['decision']='NOT_APPLICABLE'
    assert 'missing:applicability_rationale' in validate_assessor_record(rec)
