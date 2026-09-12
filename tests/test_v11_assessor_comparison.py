from pathlib import Path
import importlib.util
import yaml

ROOT=Path(__file__).resolve().parents[1]
TOOL=ROOT/"tools"/"compare_v11_assessors.py"
TEMPLATE=ROOT/"review"/"assessor-response-template-1.1-draft.yaml"
CASES=ROOT/"validation"/"INTER-RATER-CASES-1.1-DRAFT.md"
PROTOCOL=ROOT/"docs"/"ASSESSOR-PROTOCOL-ADVERSARIAL-1.1-DRAFT.md"

def _module():
    spec=importlib.util.spec_from_file_location("compare_v11_assessors",TOOL)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def _response(assessor_id):
    data=yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))
    data["assessor_id"]=assessor_id
    data["independent_completion_confirmed"]=True
    for case in data["cases"].values():
        case.update({"applicability":"APPLICABLE","result":"SATISFIED","gate_result":"PASS","confidence":"C3","rationale":"test"})
    return data

def test_inter_rater_case_ir05_uses_candidate_msp_semantics_not_adv009_score():
    text=CASES.read_text(encoding="utf-8")
    section=text.split("## Case IR-05",1)[1].split("## Case IR-06",1)[0]
    assert "MSP-005" in section and "MSP-008" in section
    assert "must not be scored separately" in section

def test_assessor_template_covers_all_cases():
    data=yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))
    assert set(data["cases"])=={"IR-01","IR-02","IR-03","IR-04","IR-05","IR-06","IR-07"}

def test_comparator_flags_critical_disagreement():
    mod=_module()
    a=_response("A")
    b=_response("B")
    b["cases"]["IR-02"]["result"]="NOT_SATISFIED"
    b["cases"]["IR-02"]["gate_result"]="BREACH"
    result=mod.compare(a,b)
    assert "IR-02" in result["critical_freeze_blockers"]
    assert result["candidate_freeze_review_result"]=="BLOCKED"


def test_assessor_protocol_does_not_score_adv009_as_standalone_candidate():
    text=PROTOCOL.read_text(encoding="utf-8")
    assert "Candidate MSP-005 / MSP-008" in text
    assert "ADV-009 is development-history only and must not be scored separately" in text
    assert "### ADV-009 —" not in text
