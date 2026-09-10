from copy import deepcopy
from pathlib import Path
import yaml
import pytest

from src.eaims.engine import assess_fixture, validate_fixture, aggregation_summary

ROOT=Path(__file__).resolve().parents[1]


def load_ri(name):
    return yaml.safe_load((ROOT/f"reference-implementations/{name}/input/fixture.yaml").read_text())


def test_partial_assessment_never_establishes_enterprise_maturity():
    r=assess_fixture(load_ri('ri-01-api-consumed-analytics'))
    assert r['assessment_type']=='PARTIAL'
    assert r['enterprise_maturity_established'] is False
    assert r['enterprise_index'] is None
    assert r['indicative_scoped_index'] is not None


def test_targeted_assessment_produces_no_overall_index():
    r=assess_fixture(load_ri('ri-02-enterprise-service-agent'))
    assert r['assessment_type']=='TARGETED'
    assert r['enterprise_maturity_established'] is False
    assert r['enterprise_index'] is None
    assert r['indicative_scoped_index'] is None


def test_duplicate_evidence_id_rejected_before_scoring():
    f=load_ri('ri-01-api-consumed-analytics')
    f['evidence'].append(deepcopy(f['evidence'][0]))
    assert 'duplicate evidence_id' in validate_fixture(f)
    with pytest.raises(ValueError): assess_fixture(f)


def test_broken_evidence_reference_rejected_before_scoring():
    f=load_ri('ri-01-api-consumed-analytics')
    f['requirement_results'][0]['evidence_refs']=['DOES-NOT-EXIST']
    assert any('references unknown evidence' in x for x in validate_fixture(f))


def test_not_applicable_requires_rationale():
    f=load_ri('ri-01-api-consumed-analytics')
    f['capabilities'][0]['applicability']='NOT_APPLICABLE'
    f['capabilities'][0].pop('applicability_rationale',None)
    assert any('NOT_APPLICABLE requires applicability_rationale' in x for x in validate_fixture(f))


def test_full_assessment_requires_all_canonical_capabilities():
    f=load_ri('ri-01-api-consumed-analytics')
    f['assessment']['assessment_type']='FULL'
    assert any('FULL assessment missing capabilities' in x for x in validate_fixture(f))

def test_unknown_gate_input_rejected():
    f=load_ri('ri-01-api-consumed-analytics')
    f.setdefault('gate_inputs',{})['G9-99']='PASS'
    assert any('unknown gate_inputs gate_id' in x for x in validate_fixture(f))


def test_satisfied_shall_requires_evidence_refs():
    f=load_ri('ri-01-api-consumed-analytics')
    f['requirement_results'][0]['evidence_refs']=[]
    assert any('SATISFIED SHALL/SHALL_NOT requires evidence_refs' in x for x in validate_fixture(f))
