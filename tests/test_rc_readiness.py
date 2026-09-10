from pathlib import Path
import yaml, json

ROOT=Path(__file__).resolve().parents[1]

def test_all_gates_bind_existing_requirements():
    reqs=yaml.safe_load((ROOT/'spec/requirements.yaml').read_text())['requirements']
    ids={r['requirement_id'] for r in reqs}
    gates=yaml.safe_load((ROOT/'spec/gates.yaml').read_text())['families']
    for fam in gates:
        for gate in fam['gates']:
            assert gate.get('requirement_ids')
            assert set(gate['requirement_ids']) <= ids

def test_critical_coverage_audit_matches_catalog():
    reqs=yaml.safe_load((ROOT/'spec/requirements.yaml').read_text())['requirements']
    expected=sum(1 for r in reqs if r['normative_level'] in ('SHALL','SHALL_NOT') and r['criticality']=='critical')
    audit=json.loads((ROOT/'validation/critical-requirement-coverage.json').read_text())
    assert audit['summary']['critical_shall_total']==expected
    assert len(audit['requirements'])==expected

def test_universal_gates_have_normative_bindings():
    gates=yaml.safe_load((ROOT/'spec/gates.yaml').read_text())['families'][0]['gates']
    assert len(gates)==10
    assert all(g['requirement_ids'] for g in gates)

def test_all_reference_evidence_respects_cutoff():
    import glob
    for name in ('ri-01-api-consumed-analytics','ri-02-enterprise-service-agent','ri-03-high-impact-decision-support'):
        d=yaml.safe_load((ROOT/f'reference-implementations/{name}/input/fixture.yaml').read_text())
        cutoff=d['assessment']['evidence_cutoff_time']
        assert all(e.get('collected_at','') <= cutoff for e in d.get('evidence',[]))

def test_fc16_core_version_is_consistent():
    core=yaml.safe_load((ROOT/'spec/core.yaml').read_text())
    assert core['spec_version']=='1.0.0-fc16'

def test_reference_golden_results_match_current_engine():
    from src.eaims.engine import assess_fixture
    import json
    for name in ('ri-01-api-consumed-analytics','ri-02-enterprise-service-agent','ri-03-high-impact-decision-support'):
        base=ROOT/f'reference-implementations/{name}'
        fixture=yaml.safe_load((base/'input/fixture.yaml').read_text())
        expected=json.loads((base/'expected/result.json').read_text())
        assert assess_fixture(fixture)==expected
