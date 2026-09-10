from pathlib import Path
import yaml
from src.eaims.engine import (
    validate_evidence, derive_risk, activated_families, evaluate_gates,
    consistency_findings, award_capability, geometric_index, assess_fixture
)

ROOT=Path(__file__).resolve().parents[1]

def ev(eid, cls="E3", conf="C3", validity="VALID", nature="SUPPORTING", collected="2026-09-09T06:00:00Z"):
    return {"evidence_id":eid,"class":cls,"confidence":conf,"validity":validity,"nature":nature,"source":"x","collected_at":collected}

def test_evidence_after_cutoff_rejected():
    assert "after_cutoff" in validate_evidence(ev("E",collected="2026-09-10T00:00:00Z"),"2026-09-09T00:00:00Z")

def test_invalidated_evidence_does_not_support_level4():
    cap={"capability_id":"X","anchor_observed":{"L1":True,"L2":True,"L3":True,"L4":True,"L5":False}}
    rr=[{"requirement_id":"R","result":"SATISFIED","criticality":"normal","evidence_refs":["E"]}]
    r=award_capability(cap,rr,[ev("E",validity="INVALIDATED")])
    assert r["result"] == "L1"

def test_e3_can_support_l4_but_not_l5():
    cap={"capability_id":"X","anchor_observed":{"L1":True,"L2":True,"L3":True,"L4":True,"L5":True}}
    rr=[{"requirement_id":"R","result":"SATISFIED","criticality":"normal","evidence_refs":["E"]}]
    r=award_capability(cap,rr,[ev("E",cls="E3")])
    assert r["result"] == "L4"

def test_e4_can_support_l5():
    cap={"capability_id":"X","anchor_observed":{"L1":True,"L2":True,"L3":True,"L4":True,"L5":True}}
    rr=[{"requirement_id":"R","result":"SATISFIED","criticality":"normal","evidence_refs":["E"]}]
    r=award_capability(cap,rr,[ev("E",cls="E4")])
    assert r["result"] == "L5"

def test_no_requirement_results_is_indeterminate():
    assert award_capability({"capability_id":"X"},[],[])["result"] == "INDETERMINATE"

def test_critical_failed_requirement_prevents_higher_award():
    cap={"capability_id":"X"}
    rr=[{"requirement_id":"R","result":"NOT_SATISFIED","criticality":"critical","evidence_refs":["E"]}]
    assert award_capability(cap,rr,[ev("E",cls="E4")])["result"] == "L2"

def test_risk_i3_a3_is_high():
    p={"impact":"I3","autonomy":"A3","reversibility":"R2","scale":"S2","velocity":"V2"}
    assert derive_risk(p)["derived_band"] == "HIGH"

def test_risk_i4_a5_can_be_critical():
    p={"impact":"I4","autonomy":"A5","reversibility":"R4","scale":"S3","velocity":"V3"}
    assert derive_risk(p)["derived_band"] == "CRITICAL"

def test_gate_family_inheritance_i3_a4():
    sys={"material":True,"agentic":True}; p=derive_risk({"impact":"I3","autonomy":"A4","reversibility":"R2","scale":"S2","velocity":"V2"})
    assert activated_families(sys,p) == ["G0","G1","G2","G3"]

def test_incomplete_gate_not_pass():
    sys={"material":True,"agentic":False}; p=derive_risk({"impact":"I2","autonomy":"A1","reversibility":"R1","scale":"S1","velocity":"V1"})
    out=evaluate_gates(sys,p,{"G1-01":"INCOMPLETE"})
    assert next(g for g in out if g["gate_id"]=="G1-01")["result"] == "INCOMPLETE"

def test_human_reserved_ai_final_authority_contradiction():
    f=consistency_findings({"human_reserved":True,"ai_final_authority":True})
    assert any(x["rule_id"]=="CONS-002" and x["severity"]=="CRITICAL" for x in f)

def test_autonomy_drift_detected():
    f=consistency_findings({"approved_autonomy":"A2","observed_autonomy":"A4"})
    assert any(x["rule_id"]=="CONS-005" for x in f)

def test_external_change_exposure_requires_reevaluation():
    f=consistency_findings({"external_change_exposure":"E3","provider_change_re_evaluation":False})
    assert any(x["rule_id"]=="CONS-004" for x in f)

def test_geometric_index_profile_first_secondary():
    assert geometric_index([{"result":"L1"},{"result":"L5"}]) == 2.24

def test_ri01_end_to_end():
    fixture=yaml.safe_load((ROOT/"reference-implementations/ri-01-api-consumed-analytics/input/fixture.yaml").read_text())
    r=assess_fixture(fixture)
    assert r["risk_profile"]["derived_band"] == "MATERIAL"
    assert next(c for c in r["capability_results"] if c["capability_id"]=="TEC-02")["result"] == "L2"
    assert next(g for g in r["gate_results"] if g["gate_id"]=="G1-03")["result"] == "BREACH"
    assert any(f["rule_id"]=="CONS-004" for f in r["consistency_findings"])

def test_not_applicable_capability_stays_out_of_index():
    cap={"capability_id":"X","applicability":"NOT_APPLICABLE"}
    r=award_capability(cap,[],[])
    assert r["result"] == "NOT_APPLICABLE"
    assert geometric_index([r,{"result":"L3"}]) == 3.0

def test_not_assessed_capability_stays_out_of_index():
    cap={"capability_id":"X","applicability":"NOT_ASSESSED"}
    r=award_capability(cap,[],[])
    assert r["result"] == "NOT_ASSESSED"
    assert geometric_index([r,{"result":"L2"}]) == 2.0

def test_conflicted_requirement_can_be_indeterminate():
    cap={"capability_id":"X"}
    rr=[{"requirement_id":"R","result":"INSUFFICIENT_EVIDENCE","criticality":"normal","evidence_refs":[],"conflict":True}]
    assert award_capability(cap,rr,[])["result"] == "INDETERMINATE"

def test_counter_evidence_does_not_raise_evidence_class():
    cap={"capability_id":"X","anchor_observed":{"L1":True,"L2":True,"L3":True,"L4":True,"L5":False}}
    rr=[{"requirement_id":"R","result":"NOT_SATISFIED","criticality":"material","evidence_refs":["E"]}]
    assert award_capability(cap,rr,[ev("E",cls="E4",nature="COUNTER")])["result"] == "L1"

def test_unverified_evidence_does_not_support_class_or_confidence_legacy_case():
    cap={"capability_id":"X","anchor_observed":{"L1":True,"L2":True,"L3":True,"L4":False,"L5":False}}
    rr=[{"requirement_id":"R","result":"SATISFIED","criticality":"normal","evidence_refs":["E"]}]
    r=award_capability(cap,rr,[ev("E",cls="E2",validity="UNVERIFIED",conf="C4")])
    assert r["result"] == "L1"
    assert r["confidence"] == "C0"

def test_i2_nonagent_only_activates_g0_g1():
    sys={"material":True,"agentic":False}; p=derive_risk({"impact":"I2","autonomy":"A1","reversibility":"R1","scale":"S2","velocity":"V1"})
    assert activated_families(sys,p) == ["G0","G1"]

def test_i1_material_only_g0():
    sys={"material":True,"agentic":False}; p=derive_risk({"impact":"I1","autonomy":"A0","reversibility":"R0","scale":"S0","velocity":"V0"})
    assert activated_families(sys,p) == ["G0"]

def test_missing_active_gate_is_incomplete():
    sys={"material":True,"agentic":False}; p=derive_risk({"impact":"I1","autonomy":"A0","reversibility":"R0","scale":"S0","velocity":"V0"})
    out=evaluate_gates(sys,p,{})
    assert next(g for g in out if g["gate_id"]=="G0-01")["result"] == "INCOMPLETE"

def test_inactive_gate_is_not_applicable():
    sys={"material":True,"agentic":False}; p=derive_risk({"impact":"I1","autonomy":"A0","reversibility":"R0","scale":"S0","velocity":"V0"})
    out=evaluate_gates(sys,p,{})
    assert next(g for g in out if g["gate_id"]=="G3-01")["result"] == "NOT_APPLICABLE"

def test_intervention_infeasibility_is_critical():
    f=consistency_findings({"human_oversight_required":True,"intervention_capacity_feasible":False})
    assert any(x["rule_id"]=="CONS-006" and x["severity"]=="CRITICAL" for x in f)

def test_result_hash_is_deterministic_for_same_fixture():
    fixture=yaml.safe_load((ROOT/"reference-implementations/ri-01-api-consumed-analytics/input/fixture.yaml").read_text())
    assert assess_fixture(fixture)["result_hash"] == assess_fixture(fixture)["result_hash"]

from src.eaims.engine import evaluate_permission_envelope, automated_agent_gate_inputs, derive_autonomy_debt

def test_ape_detects_financial_limit_breach():
    sys={"agentic":True}
    env={"allowed_tools":["refund_api"],"financial_limit":100,"external_communication_allowed":True,"delegation_allowed":False}
    events=[{"event_id":"E1","occurred_at":"2026-09-09T00:00:00Z","action":"refund","tool":"refund_api","financial_amount":250}]
    r=evaluate_permission_envelope(sys,env,events)
    assert any(v["type"]=="financial_limit_exceeded" for v in r["violations"])

def test_ape_detects_unapproved_tool():
    r=evaluate_permission_envelope({"agentic":True},{"allowed_tools":["crm"],"delegation_allowed":False,"external_communication_allowed":False},[{"event_id":"E1","occurred_at":"2026-09-09T00:00:00Z","action":"x","tool":"payment"}])
    assert any(v["type"]=="unapproved_tool" for v in r["violations"])

def test_ape_detects_unauthorized_delegation():
    r=evaluate_permission_envelope({"agentic":True},{"allowed_tools":[],"delegation_allowed":False,"external_communication_allowed":False},[{"event_id":"E1","occurred_at":"2026-09-09T00:00:00Z","action":"x","delegated":True}])
    assert any(v["type"]=="delegation_not_authorized" for v in r["violations"])

def test_automated_g3_gate_cannot_hide_financial_breach():
    sys={"agentic":True,"approved_autonomy":"A3"}
    env={"allowed_tools":["refund_api"],"financial_limit":100,"external_communication_allowed":True,"delegation_allowed":False}
    events=[{"event_id":"E1","occurred_at":"2026-09-09T00:00:00Z","action":"refund","tool":"refund_api","financial_amount":250}]
    g=automated_agent_gate_inputs(sys,env,events,{"suspension_tested":True,"escalation_path":"ops","memory_policy":"m","agent_evaluation":"e"})
    assert g["G3-04"]=="BREACH" and g["G3-10"]=="BREACH"

def test_ri02_end_to_end_detects_limit_breach_and_autonomy_debt():
    fixture=yaml.safe_load((ROOT/"reference-implementations/ri-02-enterprise-service-agent/input/fixture.yaml").read_text())
    r=assess_fixture(fixture)
    assert r["risk_profile"]["derived_band"] == "HIGH"
    assert next(g for g in r["gate_results"] if g["gate_id"]=="G3-04")["result"] == "BREACH"
    assert next(g for g in r["gate_results"] if g["gate_id"]=="G3-10")["result"] == "BREACH"
    assert any(v["type"]=="financial_limit_exceeded" for v in r["permission_envelope_evaluation"]["violations"])
    assert any(f["rule_id"]=="CONS-005" for f in r["consistency_findings"])
    assert r["autonomy_debt"]["level"] == "CRITICAL"

def test_ri02_gov04_constrained_by_critical_autonomy_failures():
    fixture=yaml.safe_load((ROOT/"reference-implementations/ri-02-enterprise-service-agent/input/fixture.yaml").read_text())
    r=assess_fixture(fixture)
    gov=next(c for c in r["capability_results"] if c["capability_id"]=="GOV-04")
    assert gov["result"] == "L2"

def test_machine_derived_g3_inputs_override_manual_pass_claim():
    fixture=yaml.safe_load((ROOT/"reference-implementations/ri-02-enterprise-service-agent/input/fixture.yaml").read_text())
    fixture["gate_inputs"]["G3-10"]="PASS"
    r=assess_fixture(fixture)
    assert next(g for g in r["gate_results"] if g["gate_id"]=="G3-10")["result"] == "BREACH"

from src.eaims.engine import evaluate_hab_controls, automated_high_impact_gate_inputs

def test_hab_detects_human_reserved_execution_by_ai():
    system={"impact":"I3"}
    policy={"human_reserved_decisions":["final_rejection"],"final_authority":"HUMAN","recourse_available":True}
    events=[{"event_id":"D1","occurred_at":"2026-09-09T00:00:00Z","decision":"final_rejection","executed_by":"AI"}]
    r=evaluate_hab_controls(system,policy,events,{"intervention_feasible":True})
    assert any(v["type"]=="human_reserved_decision_executed_by_ai" for v in r["violations"])

def test_hab_human_reserved_policy_with_human_execution_has_no_violation():
    system={"impact":"I3"}
    policy={"human_reserved_decisions":["final_rejection"],"final_authority":"HUMAN","recourse_available":True}
    events=[{"event_id":"D1","occurred_at":"2026-09-09T00:00:00Z","decision":"final_rejection","executed_by":"HUMAN"}]
    r=evaluate_hab_controls(system,policy,events,{"intervention_feasible":True})
    assert r["violations"] == []

def test_machine_derived_g2_final_authority_breach_overrides_manual_logic():
    system={"impact":"I3"}
    policy={"human_reserved_decisions":["final_rejection"],"final_authority":"HUMAN","recourse_available":True}
    events=[{"event_id":"D1","occurred_at":"2026-09-09T00:00:00Z","decision":"final_rejection","executed_by":"AI"}]
    h=evaluate_hab_controls(system,policy,events,{"intervention_feasible":True})
    g=automated_high_impact_gate_inputs(system,h,{"impact_assessment":"x","hab_defined":"x","human_competence":"x","intervention_feasible":True,"adverse_outcome_evaluation":"x","residual_risk_acceptance":"x","enhanced_monitoring":"x","independent_challenge":"x"})
    assert g["G2-03"] == "BREACH"

def test_high_impact_missing_recourse_breaches_g2_04():
    system={"impact":"I3"}
    h=evaluate_hab_controls(system,{"human_reserved_decisions":[],"final_authority":"HUMAN","recourse_available":False},[],{"intervention_feasible":True})
    g=automated_high_impact_gate_inputs(system,h,{"impact_assessment":"x","hab_defined":"x"})
    assert g["G2-04"] == "BREACH"

def test_ri03_end_to_end_detects_human_reserved_breach():
    fixture=yaml.safe_load((ROOT/"reference-implementations/ri-03-high-impact-decision-support/input/fixture.yaml").read_text())
    r=assess_fixture(fixture)
    assert r["risk_profile"]["derived_band"] == "HIGH"
    assert next(g for g in r["gate_results"] if g["gate_id"]=="G2-03")["result"] == "BREACH"
    assert any(v["type"]=="human_reserved_decision_executed_by_ai" for v in r["hab_evaluation"]["violations"])
    assert any(f["rule_id"]=="CONS-HAB-EXEC-001" for f in r["consistency_findings"])
    assert next(c for c in r["capability_results"] if c["capability_id"]=="GOV-03")["result"] == "L2"

def test_ri03_machine_g2_breach_cannot_be_hidden_by_manual_pass():
    fixture=yaml.safe_load((ROOT/"reference-implementations/ri-03-high-impact-decision-support/input/fixture.yaml").read_text())
    fixture["gate_inputs"]["G2-03"]="PASS"
    r=assess_fixture(fixture)
    assert next(g for g in r["gate_results"] if g["gate_id"]=="G2-03")["result"] == "BREACH"

def test_unverified_evidence_does_not_support_maturity():
    cap={"capability_id":"X","anchor_observed":{"L1":True,"L2":True,"L3":True,"L4":False,"L5":False}}
    rr=[{"requirement_id":"R","result":"SATISFIED","criticality":"normal","evidence_refs":["E"]}]
    r=award_capability(cap,rr,[ev("E",cls="E4",validity="UNVERIFIED",conf="C4")])
    assert r["result"] == "L1"
    assert r["confidence"] == "C0"


def test_timezone_aware_cutoff_comparison_not_lexicographic():
    # 07:00+01:00 equals 06:00Z and therefore is not after the cutoff.
    item=ev("E",collected="2026-09-09T07:00:00+01:00")
    assert "after_cutoff" not in validate_evidence(item,"2026-09-09T06:00:00Z")


def test_malformed_evidence_timestamp_rejected():
    assert "invalid:collected_at" in validate_evidence(ev("E",collected="not-a-time"),"2026-09-09T06:00:00Z")


def test_explicit_gate_not_applicable_is_preserved():
    sys={"material":True,"agentic":True}
    p=derive_risk({"impact":"I2","autonomy":"A3","reversibility":"R1","scale":"S1","velocity":"V1"})
    out=evaluate_gates(sys,p,{"G3-10":"NOT_APPLICABLE"})
    assert next(g for g in out if g["gate_id"]=="G3-10")["result"] == "NOT_APPLICABLE"


def test_external_communication_prohibition_is_valid_control():
    sys={"agentic":True,"approved_autonomy":"A3"}
    env={"allowed_tools":[],"external_communication_allowed":False,"delegation_allowed":False}
    g=automated_agent_gate_inputs(sys,env,[],{})
    assert g["G3-09"] == "PASS"


def test_false_high_impact_control_is_breach_not_incomplete():
    system={"impact":"I3"}
    h=evaluate_hab_controls(system,{"human_reserved_decisions":[],"final_authority":"HUMAN","recourse_available":True},[],{"intervention_feasible":True})
    g=automated_high_impact_gate_inputs(system,h,{"impact_assessment":False,"hab_defined":True,"human_competence":False,"independent_challenge_applicable":False})
    assert g["G2-01"] == "BREACH"
    assert g["G2-05"] == "BREACH"
    assert g["G2-10"] == "NOT_APPLICABLE"

def test_partial_satisfaction_does_not_satisfy_shall_anchor_requirement():
    cap={"capability_id":"X","anchor_observed":{"L1":True,"L2":True,"L3":True}}
    rr=[{"requirement_id":"R","result":"PARTIALLY_SATISFIED","criticality":"normal","normative_level":"SHALL","evidence_refs":["E"]}]
    r=award_capability(cap,rr,[ev("E",cls="E4")])
    assert r["result"] == "L1"


def test_counter_evidence_does_not_raise_confidence():
    cap={"capability_id":"X","anchor_observed":{"L1":True,"L2":True}}
    rr=[
        {"requirement_id":"R1","result":"SATISFIED","criticality":"normal","evidence_refs":["S"]},
        {"requirement_id":"R2","result":"NOT_SATISFIED","criticality":"normal","evidence_refs":["C"]},
    ]
    r=award_capability(cap,rr,[ev("S",cls="E1",conf="C2"),ev("C",cls="E4",conf="C4",nature="COUNTER")])
    assert r["confidence"] == "C2"
