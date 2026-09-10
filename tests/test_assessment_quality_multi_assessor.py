from pathlib import Path
import yaml
from src.eaims.assessor import (
    assess_assessment_quality, detect_multi_assessor_disagreements,
    validate_resolution_record, resolve_multi_assessor, inter_rater_dataset
)
ROOT=Path(__file__).resolve().parents[1]


def load(name):
    return yaml.safe_load((ROOT/'validation'/name).read_text(encoding='utf-8'))


def test_quality_worked_cases():
    for c in load('assessment-quality-worked-cases.yaml')['cases']:
        assert assess_assessment_quality(c['factors'])['level']==c['expected']


def test_quality_never_changes_maturity():
    q=assess_assessment_quality({'scope_completeness':1,'evidence_coverage':1,'critical_coverage':1,'confidence_profile':['C4'],'assessor_independence':'EXTERNAL'})
    assert q['maturity_effect']=='NONE'


def test_self_assessment_cannot_be_high_under_fc16_rule():
    q=assess_assessment_quality({'scope_completeness':1,'evidence_coverage':1,'critical_coverage':1,'confidence_profile':['C4'],'assessor_independence':'SELF'})
    assert q['level']=='MODERATE'
    assert 'self_assessment_limits_high_quality' in q['reasons']


def test_critical_unresolved_conflict_forces_limited():
    q=assess_assessment_quality({'scope_completeness':1,'evidence_coverage':1,'critical_coverage':1,'confidence_profile':['C4'],'assessor_independence':'EXTERNAL','critical_unresolved_conflicts':1})
    assert q['level']=='LIMITED'


def test_multi_assessor_worked_cases():
    for c in load('multi-assessor-worked-cases.yaml')['cases']:
        ds=detect_multi_assessor_disagreements(c['records'])
        assert len(ds)==1
        assert ds[0]['disagreement_class']==c['expected_disagreement_class']


def test_material_disagreement_is_not_averaged_and_can_be_resolved():
    c=next(x for x in load('multi-assessor-worked-cases.yaml')['cases'] if x['case_id']=='MA-02-MATERIAL-DISAGREEMENT')
    d=detect_multi_assessor_disagreements(c['records'])[0]
    assert set(d['decisions'])=={'SATISFIED','NOT_SATISFIED'}
    assert d['resolution_required'] is True
    r=resolve_multi_assessor(d,c['resolution'])
    assert r['status']=='RESOLVED'
    assert r['final_decision']=='NOT_SATISFIED'
    assert len(r['original_records'])==2


def test_resolution_requires_all_assessors_to_be_considered():
    c=next(x for x in load('multi-assessor-worked-cases.yaml')['cases'] if x['case_id']=='MA-02-MATERIAL-DISAGREEMENT')
    d=detect_multi_assessor_disagreements(c['records'])[0]
    bad=dict(c['resolution']); bad['considered_assessor_ids']=['A-01']
    assert 'missing:considered_assessor_ids' in validate_resolution_record(bad,d)


def test_inter_rater_export_preserves_independent_records():
    c=next(x for x in load('multi-assessor-worked-cases.yaml')['cases'] if x['case_id']=='MA-02-MATERIAL-DISAGREEMENT')
    rows=inter_rater_dataset(c['records'])
    assert len(rows)==2
    assert {r['decision'] for r in rows}=={'SATISFIED','NOT_SATISFIED'}
    assert all('independence_class' in r for r in rows)
