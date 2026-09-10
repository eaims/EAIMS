from pathlib import Path
import yaml
from src.eaims.engine import award_capability, apply_cross_capability_dependencies

ROOT=Path(__file__).resolve().parents[1]

def ev(eid, cls='E3', nature='SUPPORTING', severity=None):
    x={'evidence_id':eid,'class':cls,'confidence':'C3','validity':'VALID','nature':nature,'source':'test','collected_at':'2026-09-09T00:00:00Z'}
    if severity: x['severity']=severity
    return x

def rr(rid,result='SATISFIED',refs=None,criticality='material'):
    return {'requirement_id':rid,'result':result,'evidence_refs':refs or [],'criticality':criticality}

def test_all_30_capabilities_have_150_anchor_eligibility_rules():
    d=yaml.safe_load((ROOT/'spec/anchor-eligibility.yaml').read_text())
    assert len(d['capabilities'])==30
    assert sum(len(c['levels']) for c in d['capabilities'])==150
    assert all(set(c['levels'])=={'L1','L2','L3','L4','L5'} for c in d['capabilities'])

def test_l4_requires_two_operating_cycles_for_canonical_capability():
    cap={'capability_id':'OPS-03','anchor_observed':{'L1':True,'L2':True,'L3':True,'L4':True,'L5':False},'operating_cycles':1}
    reqs=yaml.safe_load((ROOT/'spec/anchor-eligibility.yaml').read_text())
    rule=next(c for c in reqs['capabilities'] if c['capability_id']=='OPS-03')
    rrs=[rr(rid,refs=['E']) for rid in rule['levels']['L4']['required_requirements']]
    out=award_capability(cap,rrs,[ev('E','E3')])
    assert out['result']!='L4'
    assert out['anchor_eligibility_trace']['levels']['L4']['operating_cycles_ok'] is False

def test_l5_requires_adaptation_cycle_even_with_e4():
    cap={'capability_id':'ADO-02','anchor_observed':{x:True for x in ('L1','L2','L3','L4','L5')},'operating_cycles':2,'adaptation_cycles':0}
    spec=yaml.safe_load((ROOT/'spec/anchor-eligibility.yaml').read_text())
    rule=next(c for c in spec['capabilities'] if c['capability_id']=='ADO-02')
    rrs=[rr(rid,refs=['E']) for rid in rule['levels']['L5']['required_requirements']]
    out=award_capability(cap,rrs,[ev('E','E4')])
    assert out['result']!='L5'
    assert out['anchor_eligibility_trace']['levels']['L5']['adaptation_cycles_ok'] is False

def test_higher_order_observation_is_preserved_when_prerequisite_blocks():
    cap={'capability_id':'GOV-03','anchor_observed':{'L1':True,'L2':True,'L3':True,'L4':True,'L5':False}}
    out=award_capability(cap,[rr('EAIMS-HAB-002',refs=['E']),rr('EAIMS-HAB-003','NOT_SATISFIED',['E'],criticality='critical')],[ev('E','E3')])
    assert 'L3' in out['higher_order_observations_preserved'] or 'L4' in out['higher_order_observations_preserved']

def test_material_counter_evidence_blocks_managed_level():
    cap={'capability_id':'TEC-02','anchor_observed':{'L1':True,'L2':True,'L3':True,'L4':True,'L5':False},'operating_cycles':3}
    spec=yaml.safe_load((ROOT/'spec/anchor-eligibility.yaml').read_text())
    rule=next(c for c in spec['capabilities'] if c['capability_id']=='TEC-02')
    required=rule['levels']['L4']['required_requirements']
    rrs=[rr(rid,refs=['S']) for rid in required]
    rrs[0]['evidence_refs'].append('C')
    out=award_capability(cap,rrs,[ev('S','E3'),ev('C','E3','COUNTER','material')])
    assert out['result']!='L4'
    assert out['anchor_eligibility_trace']['levels']['L4']['counter_evidence_ok'] is False

def test_hard_cross_capability_dependency_constrains_only_when_both_assessed():
    results=[{'capability_id':'GOV-04','result':'L4'},{'capability_id':'OPS-02','result':'L2'}]
    out,findings=apply_cross_capability_dependencies(results,[{'capability_id':'GOV-04'},{'capability_id':'OPS-02'}],{'agentic':True})
    gov=next(x for x in out if x['capability_id']=='GOV-04')
    assert gov['raw_result']=='L4' and gov['result']=='L3'
    assert any(f['rule_id']=='DEP-AUT-001' for f in findings)

def test_missing_dependency_in_partial_scope_does_not_silently_cap():
    results=[{'capability_id':'GOV-04','result':'L4'}]
    out,findings=apply_cross_capability_dependencies(results,[{'capability_id':'GOV-04'}],{'agentic':True})
    assert out[0]['result']=='L4'
    assert findings==[]
