from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from .paths import ROOT
from typing import Any
import json, math, yaml


LEVEL_NUM = {f"L{i}": i for i in range(1,6)}
IMPACT_NUM = {f"I{i}": i for i in range(5)}
AUTONOMY_NUM = {f"A{i}": i for i in range(6)}
REV_NUM = {f"R{i}": i for i in range(5)}
SCALE_NUM = {f"S{i}": i for i in range(5)}
VELOCITY_NUM = {f"V{i}": i for i in range(5)}
CONF_NUM = {f"C{i}": i for i in range(5)}
CLASS_NUM = {f"E{i}": i for i in range(1,5)}
VALIDITY_CURRENT = {"VALID"}
COUNTER_VALIDITY = {"VALID", "CONFLICTED"}


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def content_hash(obj: Any) -> str:
    return sha256(canonical_bytes(obj)).hexdigest()


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def evidence_index(evidence: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {e["evidence_id"]: e for e in evidence}


def _parse_timestamp(value: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("timestamp must be a non-empty ISO 8601 string")
    normalized = value.strip().replace("Z", "+00:00")
    dt = datetime.fromisoformat(normalized)
    if dt.tzinfo is None:
        raise ValueError("timestamp must include a UTC offset or Z")
    return dt.astimezone(timezone.utc)


def validate_evidence(e: dict[str, Any], cutoff: str | None = None) -> list[str]:
    errors=[]
    required=("evidence_id","class","confidence","validity","nature","source","collected_at")
    for k in required:
        if k not in e: errors.append(f"missing:{k}")
    if not str(e.get("evidence_id", "")).strip(): errors.append("invalid:evidence_id")
    if e.get("class") not in CLASS_NUM: errors.append("invalid:class")
    if e.get("confidence") not in CONF_NUM: errors.append("invalid:confidence")
    if e.get("validity") not in {"VALID","STALE","INVALIDATED","CONFLICTED","UNVERIFIED"}: errors.append("invalid:validity")
    if e.get("nature") not in {"SUPPORTING","COUNTER","ABSENCE","CONTEXT"}: errors.append("invalid:nature")
    if not str(e.get("source", "")).strip(): errors.append("invalid:source")
    collected = e.get("collected_at")
    if collected:
        try:
            collected_dt = _parse_timestamp(collected)
        except (TypeError, ValueError):
            errors.append("invalid:collected_at")
            collected_dt = None
        if cutoff and collected_dt is not None:
            try:
                cutoff_dt = _parse_timestamp(cutoff)
            except (TypeError, ValueError):
                errors.append("invalid:cutoff")
            else:
                if collected_dt > cutoff_dt:
                    errors.append("after_cutoff")
    return errors


def current_supporting(e: dict[str, Any]) -> bool:
    return e.get("nature") == "SUPPORTING" and e.get("validity") in VALIDITY_CURRENT


def max_evidence_class(evidence: list[dict[str, Any]], refs: list[str]) -> int:
    idx=evidence_index(evidence)
    vals=[CLASS_NUM[idx[r]["class"]] for r in refs if r in idx and current_supporting(idx[r])]
    return max(vals, default=0)


def confidence_from_evidence(evidence: list[dict[str, Any]], refs: list[str]) -> str:
    idx=evidence_index(evidence)
    vals=[CONF_NUM[idx[r]["confidence"]] for r in refs if r in idx and current_supporting(idx[r])]
    if not vals: return "C0"
    # Conservative: capability confidence cannot exceed the weakest valid supporting evidence used.
    return f"C{min(vals)}"


def generic_level_eligibility(requirement_results: list[dict[str, Any]], evidence: list[dict[str, Any]]) -> dict[str,bool]:
    """Fallback policy for non-canonical/ad-hoc capabilities used by unit tests and extensions."""
    refs=[]
    failed_critical=False
    insufficient=False
    partial_shall=False
    for rr in requirement_results:
        refs += rr.get("evidence_refs",[]) or []
        if rr.get("criticality") == "critical" and rr.get("result") == "NOT_SATISFIED": failed_critical=True
        if rr.get("result") == "INSUFFICIENT_EVIDENCE": insufficient=True
        if rr.get("result") == "PARTIALLY_SATISFIED" and rr.get("normative_level") in {"SHALL","SHALL_NOT"}:
            insufficient=True
            partial_shall=True
    mx=max_evidence_class(evidence, refs)
    return {
        "L1": True,
        "L2": mx >= 1 and not partial_shall,
        "L3": mx >= 2 and not failed_critical and not insufficient,
        "L4": mx >= 3 and not failed_critical and not insufficient,
        "L5": mx >= 4 and not failed_critical and not insufficient,
    }


def _anchor_spec_index() -> dict[str, dict[str, Any]]:
    path=ROOT/"spec"/"anchor-eligibility.yaml"
    if not path.exists():
        return {}
    return {x["capability_id"]:x for x in load_yaml(path).get("capabilities",[])}


def _severity_rank(value: str | None) -> int:
    return {"minor":1,"normal":1,"material":2,"critical":3}.get(str(value or "minor").lower(),1)


def capability_anchor_eligibility(capability: dict[str, Any], requirement_results: list[dict[str, Any]], evidence: list[dict[str, Any]]) -> tuple[dict[str,bool],dict[str,Any]]:
    """Evaluate canonical capability-specific L1-L5 eligibility.

    Eligibility combines explicit anchor observation, requirement satisfaction, evidence class,
    operating/adaptation cycles, and unresolved counter-evidence. It deliberately keeps higher-order
    evidence visible even when a prerequisite blocks the awarded level.
    """
    spec=_anchor_spec_index().get(capability.get("capability_id"))
    if not spec:
        return generic_level_eligibility(requirement_results,evidence), {"mode":"generic_fallback"}

    rr_by={r["requirement_id"]:r for r in requirement_results}
    evidx=evidence_index(evidence)
    refs=sorted({ref for r in requirement_results for ref in (r.get("evidence_refs",[]) or [])})
    mx=max_evidence_class(evidence,refs)
    operating_cycles=int(capability.get("operating_cycles",0) or 0)
    adaptation_cycles=int(capability.get("adaptation_cycles",0) or 0)
    observed=capability.get("anchor_observed",{}) or {}

    # Determine strongest unresolved counter-evidence linked to this capability.
    strongest_counter=0
    counter_refs=[]
    for rr in requirement_results:
        sev=_severity_rank(rr.get("criticality"))
        for ref in rr.get("evidence_refs",[]) or []:
            e=evidx.get(ref)
            if e and e.get("nature")=="COUNTER" and e.get("validity") in COUNTER_VALIDITY:
                strongest_counter=max(strongest_counter,_severity_rank(e.get("severity")) if e.get("severity") else sev)
                counter_refs.append(ref)

    eligibility={}
    details={"mode":"capability_specific","max_supporting_evidence_class":f"E{mx}" if mx else None,
             "operating_cycles":operating_cycles,"adaptation_cycles":adaptation_cycles,
             "counter_evidence_refs":sorted(set(counter_refs)),"levels":{}}
    previous=True
    for lvl in ("L1","L2","L3","L4","L5"):
        rule=spec["levels"][lvl]
        required=rule.get("required_requirements",[]) or []
        missing=[]; failed=[]; insufficient=[]
        for rid in required:
            rr=rr_by.get(rid)
            if rr is None:
                missing.append(rid)
            elif rr.get("result") == "NOT_SATISFIED":
                failed.append(rid)
            elif rr.get("result") in {"INSUFFICIENT_EVIDENCE"}:
                insufficient.append(rid)
            elif rr.get("result") == "PARTIALLY_SATISFIED" and rr.get("normative_level") in {"SHALL","SHALL_NOT"}:
                insufficient.append(rid)
            elif rr.get("result") not in {"SATISFIED","PARTIALLY_SATISFIED"}:
                missing.append(rid)
        mincls=rule.get("minimum_evidence_class")
        evidence_ok=True if not mincls else mx >= CLASS_NUM[mincls]
        cycles_ok=operating_cycles >= int(rule.get("minimum_operating_cycles",0) or 0)
        adapt_ok=adaptation_cycles >= int(rule.get("minimum_adaptation_cycles",0) or 0)
        threshold=_severity_rank(rule.get("max_unresolved_counter_evidence","critical"))
        counter_ok=strongest_counter <= threshold
        obs_ok=True if lvl not in observed else bool(observed[lvl])
        req_ok=not (missing or failed or insufficient)
        ok=bool(previous and obs_ok and evidence_ok and cycles_ok and adapt_ok and req_ok and counter_ok)
        eligibility[lvl]=ok
        details["levels"][lvl]={"eligible":ok,"anchor_observed":obs_ok,"evidence_ok":evidence_ok,
            "operating_cycles_ok":cycles_ok,"adaptation_cycles_ok":adapt_ok,"requirements_ok":req_ok,
            "counter_evidence_ok":counter_ok,"missing_requirements":missing,"failed_requirements":failed,
            "insufficient_requirements":insufficient,"minimum_evidence_class":mincls,
            "minimum_operating_cycles":rule.get("minimum_operating_cycles",0),
            "minimum_adaptation_cycles":rule.get("minimum_adaptation_cycles",0)}
        previous=ok
    return eligibility,details


def award_capability(capability: dict[str, Any], requirement_results: list[dict[str, Any]], evidence: list[dict[str, Any]]) -> dict[str, Any]:
    applicable = capability.get("applicability", "APPLICABLE")
    if applicable == "NOT_APPLICABLE": return {"capability_id":capability["capability_id"],"result":"NOT_APPLICABLE"}
    if applicable == "NOT_ASSESSED": return {"capability_id":capability["capability_id"],"result":"NOT_ASSESSED"}
    if not requirement_results: return {"capability_id":capability["capability_id"],"result":"INDETERMINATE","rationale":"No requirement results supplied."}
    conflicted = any(r.get("result") == "INSUFFICIENT_EVIDENCE" and r.get("conflict",False) for r in requirement_results)
    if conflicted:
        return {"capability_id":capability["capability_id"],"result":"INDETERMINATE","rationale":"Material evidence conflict unresolved."}
    eligibility,anchor_trace=capability_anchor_eligibility(capability,requirement_results,evidence)
    awarded="INDETERMINATE"
    for l in ("L1","L2","L3","L4","L5"):
        if eligibility[l]: awarded=l
        else: break
    refs=[]
    for r in requirement_results: refs += r.get("evidence_refs",[]) or []
    confidence=confidence_from_evidence(evidence,refs)
    blocked=[r["requirement_id"] for r in requirement_results if r.get("result") in {"NOT_SATISFIED","INSUFFICIENT_EVIDENCE"}]
    # Preserve observed higher-order evidence even if prerequisite eligibility blocks award.
    higher=[]
    observed=capability.get("anchor_observed",{}) or {}
    for lvl in ("L2","L3","L4","L5"):
        if observed.get(lvl) is True and not eligibility.get(lvl):
            higher.append(lvl)
    return {
        "capability_id": capability["capability_id"],
        "result": awarded,
        "confidence": confidence,
        "eligible_levels": eligibility,
        "anchor_eligibility_trace": anchor_trace,
        "higher_order_observations_preserved": higher,
        "blocked_by": blocked,
        "evidence_refs": sorted(set(refs)),
    }


def apply_cross_capability_dependencies(capability_results: list[dict[str,Any]], capabilities: list[dict[str,Any]], system: dict[str,Any]) -> tuple[list[dict[str,Any]],list[dict[str,Any]]]:
    """Apply the small explicit dependency catalog after local capability awards.

    Hard dependencies can constrain a target only when both capabilities are actually assessed.
    Supporting dependencies create findings but never silently alter maturity.
    """
    path=ROOT/"spec"/"anchor-eligibility.yaml"
    if not path.exists(): return capability_results,[]
    dep_rules=load_yaml(path).get("dependencies",[])
    byres={r["capability_id"]:r for r in capability_results}
    bycap={c["capability_id"]:c for c in capabilities}
    findings=[]
    for d in dep_rules:
        target=byres.get(d["capability_id"]); prereq=byres.get(d["dependency_capability"])
        if not target or not prereq: continue
        tv=LEVEL_NUM.get(target.get("result"),0); pv=LEVEL_NUM.get(prereq.get("result"),0)
        if tv < LEVEL_NUM[d["target_level"]]: continue
        if pv >= LEVEL_NUM[d["minimum_level"]]: continue
        finding={"rule_id":d["rule_id"],"severity":"MATERIAL" if d["type"]=="hard" else "WARNING",
                 "message":d["rationale"],"target_capability":d["capability_id"],
                 "dependency_capability":d["dependency_capability"],"dependency_type":d["type"]}
        findings.append(finding)
        if d["type"]=="hard":
            # constrain to immediately below dependency-trigger target level, preserving local raw result
            target.setdefault("raw_result",target["result"])
            cap=max(1,LEVEL_NUM[d["target_level"]]-1)
            target["result"]=f"L{min(tv,cap)}"
            target.setdefault("dependency_constraints",[]).append(d["rule_id"])
    return capability_results,findings

def derive_risk(profile: dict[str, Any]) -> dict[str, Any]:
    impact=IMPACT_NUM[profile["impact"]]
    autonomy=AUTONOMY_NUM[profile["autonomy"]]
    rev=REV_NUM[profile["reversibility"]]
    scale=SCALE_NUM[profile["scale"]]
    velocity=VELOCITY_NUM[profile["velocity"]]
    rank=0
    if impact >= 1: rank=1
    if impact >= 2: rank=2
    if impact >= 3 and autonomy >= 3: rank=max(rank,3)
    if impact == 4: rank=max(rank,3)
    if impact >= 3 and rev >= 3: rank=max(rank,3)
    if autonomy >= 4 and velocity >= 3 and scale >= 3: rank=max(rank,3)
    if impact == 4 and autonomy >= 4 and (rev >=3 or scale >=3): rank=4
    bands=["LOW","MODERATE","MATERIAL","HIGH","CRITICAL"]
    effects=[]
    if impact >=3 and rev>=3: effects.append("activate_high_impact_governance")
    if autonomy>=4 and velocity>=3: effects.append("activate_agentic_critical_controls")
    if autonomy>=4 and velocity>=3 and scale>=3: effects.append("activate_selected_G2_assurance_controls")
    return {**profile,"derived_band":bands[rank],"escalation_effects":effects}


def activated_families(system: dict[str, Any], risk: dict[str, Any]) -> list[str]:
    fam=[]
    material=IMPACT_NUM[risk["impact"]] >= 1 or bool(system.get("material",False))
    if material: fam.append("G0")
    if IMPACT_NUM[risk["impact"]] >=2: fam.append("G1")
    if IMPACT_NUM[risk["impact"]] >=3 or "activate_selected_G2_assurance_controls" in risk.get("escalation_effects",[]): fam.append("G2")
    if bool(system.get("agentic")) or AUTONOMY_NUM[risk["autonomy"]] >=3: fam.append("G3")
    return fam


def evaluate_gates(system: dict[str, Any], risk: dict[str, Any], gate_inputs: dict[str, Any]) -> list[dict[str, Any]]:
    spec=load_yaml(ROOT/"spec"/"gates.yaml")
    active=set(activated_families(system,risk))
    out=[]
    for family in spec["families"]:
        for g in family["gates"]:
            gid=g["gate_id"]
            if family["family"] not in active:
                result="NOT_APPLICABLE"; reason="Gate family not activated by context."
            elif gid not in gate_inputs:
                result="INCOMPLETE"; reason="No evidence-backed gate assertion supplied."
            else:
                val=gate_inputs[gid]
                if val is True or val == "PASS": result="PASS"; reason="Applicable control demonstrated."
                elif val is False or val == "BREACH": result="BREACH"; reason="Applicable control demonstrably not satisfied."
                elif val == "NOT_APPLICABLE": result="NOT_APPLICABLE"; reason="Gate is conditionally not applicable in this activated family."
                else: result="INCOMPLETE"; reason="Evidence insufficient to establish pass or breach."
            out.append({"gate_id":gid,"family":family["family"],"title":g["title"],"result":result,"reason":reason})
    return out


def consistency_findings(ctx: dict[str, Any]) -> list[dict[str,Any]]:
    findings=[]
    if ctx.get("human_reserved") is True and ctx.get("ai_final_authority") is True:
        findings.append({"rule_id":"CONS-002","severity":"CRITICAL","message":"A Human Reserved decision cannot assign final authority to AI."})
    a=ctx.get("approved_autonomy"); o=ctx.get("observed_autonomy")
    if a in AUTONOMY_NUM and o in AUTONOMY_NUM and AUTONOMY_NUM[a] < AUTONOMY_NUM[o]:
        findings.append({"rule_id":"CONS-005","severity":"CRITICAL","message":"Observed autonomy exceeds approved autonomy."})
    if ctx.get("human_oversight_required") is True and ctx.get("intervention_capacity_feasible") is False:
        findings.append({"rule_id":"CONS-006","severity":"CRITICAL","message":"Nominal human oversight is operationally infeasible."})
    if ctx.get("external_change_exposure") in {"E3","E4"} and ctx.get("provider_change_re_evaluation") is False:
        findings.append({"rule_id":"CONS-004","severity":"MATERIAL","message":"High external change exposure requires provider-change re-evaluation controls."})
    return findings



def evaluate_permission_envelope(system: dict[str, Any], envelope: dict[str, Any] | None, events: list[dict[str, Any]]) -> dict[str, Any]:
    """Evaluate a small, deterministic subset of an Agent Permission Envelope (APE).

    The FC16 reference engine intentionally checks only objectively machine-testable
    boundaries: allowed tools, financial limits, external communication authority,
    delegation permission, and basic audit fields. Human/contextual authority remains
    assessor-evaluated through EAIMS requirement results and HAB records.
    """
    if not system.get("agentic"):
        return {"applicable": False, "violations": [], "auditability_complete": True}
    if not envelope:
        return {"applicable": True, "violations": [{"type":"missing_permission_envelope","severity":"CRITICAL"}], "auditability_complete": False}
    allowed_tools=set(envelope.get("allowed_tools",[]) or [])
    financial_limit=envelope.get("financial_limit")
    external_allowed=bool(envelope.get("external_communication_allowed",False))
    delegation_allowed=bool(envelope.get("delegation_allowed",False))
    violations=[]
    auditability_complete=True
    for ev in events:
        required=("event_id","occurred_at","action")
        if any(not ev.get(k) for k in required):
            auditability_complete=False
            violations.append({"type":"audit_record_incomplete","severity":"MATERIAL","event_id":ev.get("event_id")})
        tool=ev.get("tool")
        if tool and tool not in allowed_tools:
            violations.append({"type":"unapproved_tool","severity":"CRITICAL","event_id":ev.get("event_id"),"tool":tool})
        amount=ev.get("financial_amount")
        if amount is not None and financial_limit is not None and float(amount) > float(financial_limit):
            violations.append({"type":"financial_limit_exceeded","severity":"CRITICAL","event_id":ev.get("event_id"),"observed":amount,"approved":financial_limit})
        if ev.get("external_communication") and not external_allowed:
            violations.append({"type":"external_communication_not_authorized","severity":"CRITICAL","event_id":ev.get("event_id")})
        if ev.get("delegated") and not delegation_allowed:
            violations.append({"type":"delegation_not_authorized","severity":"CRITICAL","event_id":ev.get("event_id")})
    return {"applicable": True, "violations": violations, "auditability_complete": auditability_complete}


def automated_agent_gate_inputs(system: dict[str, Any], envelope: dict[str, Any] | None, events: list[dict[str, Any]], controls: dict[str, Any] | None = None) -> dict[str, Any]:
    if not system.get("agentic"):
        return {}
    controls=controls or {}
    ape=evaluate_permission_envelope(system,envelope,events)
    vtypes={v["type"] for v in ape["violations"]}
    out={
        "G3-01": "PASS" if system.get("approved_autonomy") or system.get("autonomy") else "INCOMPLETE",
        "G3-02": "BREACH" if "missing_permission_envelope" in vtypes else "PASS",
        "G3-03": "PASS" if envelope and envelope.get("allowed_tools") else "INCOMPLETE",
        "G3-04": "BREACH" if vtypes & {"financial_limit_exceeded","unapproved_tool","external_communication_not_authorized","delegation_not_authorized"} else "PASS",
        "G3-05": "BREACH" if "delegation_not_authorized" in vtypes else ("PASS" if envelope and "delegation_allowed" in envelope else "INCOMPLETE"),
        "G3-06": "PASS" if ape["auditability_complete"] and events else "INCOMPLETE",
        "G3-07": "PASS" if controls.get("suspension_tested") is True else ("BREACH" if controls.get("suspension_tested") is False else "INCOMPLETE"),
        "G3-08": "PASS" if controls.get("escalation_path") else "INCOMPLETE",
        "G3-09": "BREACH" if "external_communication_not_authorized" in vtypes else ("PASS" if envelope and "external_communication_allowed" in envelope else "INCOMPLETE"),
        "G3-10": "BREACH" if "financial_limit_exceeded" in vtypes else ("PASS" if envelope and envelope.get("financial_limit") is not None else "NOT_APPLICABLE"),
        "G3-11": "PASS" if not system.get("persistent_memory") or controls.get("memory_policy") else "INCOMPLETE",
        "G3-12": "PASS" if controls.get("agent_evaluation") else "INCOMPLETE",
    }
    return out



def evaluate_hab_controls(system: dict[str, Any], decision_policy: dict[str, Any] | None, decision_events: list[dict[str, Any]], controls: dict[str, Any] | None = None) -> dict[str, Any]:
    """Deterministic checks for the machine-verifiable subset of a Human Accountability Boundary.

    FC16 checks explicit final authority, Human Reserved decision enforcement, recourse,
    intervention feasibility, and decision auditability. Competence, fairness, and
    substantive appropriateness remain hybrid/human-assessed.
    """
    controls=controls or {}
    decision_policy=decision_policy or {}
    hr=set(decision_policy.get("human_reserved_decisions",[]) or [])
    final_authority=decision_policy.get("final_authority")
    violations=[]
    auditability_complete=True
    for ev in decision_events:
        if any(not ev.get(k) for k in ("event_id","occurred_at","decision","executed_by")):
            auditability_complete=False
            violations.append({"type":"decision_audit_record_incomplete","severity":"MATERIAL","event_id":ev.get("event_id")})
        if ev.get("decision") in hr and str(ev.get("executed_by","")).upper() == "AI":
            violations.append({"type":"human_reserved_decision_executed_by_ai","severity":"CRITICAL","event_id":ev.get("event_id"),"decision":ev.get("decision")})
    if hr and str(final_authority or "").upper() == "AI":
        violations.append({"type":"human_reserved_final_authority_assigned_to_ai","severity":"CRITICAL"})
    return {
        "applicable": bool(hr) or IMPACT_NUM.get(system.get("impact","I0"),0) >= 3,
        "human_reserved_decisions": sorted(hr),
        "final_authority": final_authority,
        "recourse_available": bool(decision_policy.get("recourse_available")),
        "intervention_feasible": controls.get("intervention_feasible"),
        "violations": violations,
        "auditability_complete": auditability_complete,
    }


def automated_high_impact_gate_inputs(system: dict[str, Any], hab_eval: dict[str, Any], controls: dict[str, Any] | None = None) -> dict[str, Any]:
    """Derive machine-checkable G2 assertions; observed violations override manual assertions."""
    controls=controls or {}
    if IMPACT_NUM.get(system.get("impact","I0"),0) < 3:
        return {}

    def control_state(key: str) -> str:
        if key not in controls or controls.get(key) is None:
            return "INCOMPLETE"
        return "PASS" if bool(controls.get(key)) else "BREACH"

    vtypes={v["type"] for v in hab_eval.get("violations",[])}
    final_breach=bool(vtypes & {"human_reserved_decision_executed_by_ai","human_reserved_final_authority_assigned_to_ai"})
    independent_applicable = controls.get("independent_challenge_applicable")
    if independent_applicable is False:
        independent_state = "NOT_APPLICABLE"
    elif independent_applicable is True:
        independent_state = control_state("independent_challenge")
    else:
        independent_state = "INCOMPLETE"
    return {
        "G2-01": control_state("impact_assessment"),
        "G2-02": control_state("hab_defined"),
        "G2-03": "BREACH" if final_breach else ("PASS" if hab_eval.get("final_authority") else "INCOMPLETE"),
        "G2-04": "PASS" if hab_eval.get("recourse_available") else "BREACH",
        "G2-05": control_state("human_competence"),
        "G2-06": "PASS" if hab_eval.get("intervention_feasible") is True else ("BREACH" if hab_eval.get("intervention_feasible") is False else "INCOMPLETE"),
        "G2-07": control_state("adverse_outcome_evaluation"),
        "G2-08": control_state("residual_risk_acceptance"),
        "G2-09": control_state("enhanced_monitoring"),
        "G2-10": independent_state,
    }

def derive_autonomy_debt(system: dict[str, Any], capability_results: list[dict[str, Any]], gate_results: list[dict[str, Any]], permission_eval: dict[str, Any] | None = None) -> dict[str, Any]:
    """Qualitative, deliberately non-calibrated diagnostic for FC16."""
    autonomy=AUTONOMY_NUM.get(system.get("observed_autonomy") or system.get("approved_autonomy") or system.get("autonomy","A0"),0)
    levels={r["capability_id"]:LEVEL_NUM.get(r.get("result"),0) for r in capability_results}
    support=[levels.get("GOV-04",0),levels.get("GOV-03",0),levels.get("OPS-02",0),levels.get("OPS-03",0)]
    support=[x for x in support if x]
    floor=min(support) if support else 0
    critical_agent_breaches=sum(1 for g in gate_results if g["family"]=="G3" and g["result"]=="BREACH")
    violations=len((permission_eval or {}).get("violations",[]))
    if autonomy <= 2 and not critical_agent_breaches and not violations:
        level="NONE"
    elif critical_agent_breaches >= 2 or violations >= 1 or (autonomy >=4 and floor and floor <=2):
        level="CRITICAL"
    elif critical_agent_breaches == 1 or (autonomy >=3 and (floor==0 or floor<=2)):
        level="MATERIAL"
    else:
        level="MODERATE"
    return {"level":level,"autonomy_level":f"A{autonomy}","supporting_maturity_floor":floor or None,"agent_gate_breaches":critical_agent_breaches,"permission_violations":violations,"calibration":"design-diagnostic-not-empirically-calibrated"}


def geometric_index(capability_results: list[dict[str,Any]]) -> float | None:
    vals=[LEVEL_NUM[r["result"]] for r in capability_results if r.get("result") in LEVEL_NUM]
    if not vals: return None
    return round(math.exp(sum(math.log(v) for v in vals)/len(vals)),2)



def validate_fixture(fixture: dict[str, Any]) -> list[str]:
    """Validate an executable assessment fixture before scoring.

    This is intentionally stricter than permissive YAML parsing: duplicate identifiers,
    unknown canonical references, broken evidence references, invalid assessment scope,
    and malformed timestamps are rejected before any maturity result is produced.
    """
    errors: list[str] = []
    if not isinstance(fixture, dict):
        return ["fixture must be an object"]
    assessment = fixture.get("assessment")
    if not isinstance(assessment, dict):
        return ["assessment is required"]
    for key in ("assessment_id", "assessment_type", "evidence_cutoff_time"):
        if not assessment.get(key):
            errors.append(f"assessment.{key} is required")
    atype = assessment.get("assessment_type")
    if atype not in {"FULL", "PARTIAL", "TARGETED"}:
        errors.append("assessment.assessment_type must be FULL, PARTIAL, or TARGETED")
    cutoff = assessment.get("evidence_cutoff_time")
    if cutoff:
        try:
            _parse_timestamp(cutoff)
        except (TypeError, ValueError):
            errors.append("assessment.evidence_cutoff_time must be timezone-aware ISO 8601")

    if not isinstance(fixture.get("system"), dict):
        errors.append("system is required")
    risk = fixture.get("risk_profile")
    if not isinstance(risk, dict):
        errors.append("risk_profile is required")
    else:
        expected = {
            "impact": IMPACT_NUM, "autonomy": AUTONOMY_NUM, "reversibility": REV_NUM,
            "scale": SCALE_NUM, "velocity": VELOCITY_NUM,
        }
        for key, enum in expected.items():
            if risk.get(key) not in enum:
                errors.append(f"risk_profile.{key} is invalid or missing")

    canonical_caps = {c["capability_id"] for c in load_yaml(ROOT / "spec" / "capabilities.yaml")["capabilities"]}
    canonical_reqs = {r["requirement_id"] for r in load_yaml(ROOT / "spec" / "requirements.yaml")["requirements"]}

    evidence = fixture.get("evidence", [])
    if not isinstance(evidence, list):
        errors.append("evidence must be an array")
        evidence = []
    eids = [e.get("evidence_id") for e in evidence if isinstance(e, dict)]
    if len(eids) != len(set(eids)):
        errors.append("duplicate evidence_id")
    evidence_ids = {x for x in eids if x}
    for e in evidence:
        if not isinstance(e, dict):
            errors.append("evidence entries must be objects")
            continue
        for err in validate_evidence(e, cutoff):
            errors.append(f"evidence.{e.get('evidence_id','?')}:{err}")

    caps = fixture.get("capabilities", [])
    if not isinstance(caps, list):
        errors.append("capabilities must be an array")
        caps = []
    cap_ids = [c.get("capability_id") for c in caps if isinstance(c, dict)]
    if len(cap_ids) != len(set(cap_ids)):
        errors.append("duplicate capability_id in fixture")
    for c in caps:
        if not isinstance(c, dict):
            errors.append("capability entries must be objects")
            continue
        cid = c.get("capability_id")
        if cid not in canonical_caps:
            errors.append(f"unknown capability_id {cid}")
        app = c.get("applicability", "APPLICABLE")
        if app not in {"APPLICABLE", "CONDITIONALLY_APPLICABLE", "NOT_APPLICABLE", "NOT_ASSESSED"}:
            errors.append(f"{cid} has invalid applicability")
        if app == "NOT_APPLICABLE" and not str(c.get("applicability_rationale", "")).strip():
            errors.append(f"{cid} NOT_APPLICABLE requires applicability_rationale")

    if atype == "FULL" and set(cap_ids) != canonical_caps:
        missing = sorted(canonical_caps - set(cap_ids))
        extra = sorted(set(cap_ids) - canonical_caps)
        if missing:
            errors.append("FULL assessment missing capabilities: " + ", ".join(missing))
        if extra:
            errors.append("FULL assessment contains non-canonical capabilities: " + ", ".join(extra))

    req_results = fixture.get("requirement_results", [])
    if not isinstance(req_results, list):
        errors.append("requirement_results must be an array")
        req_results = []
    rr_ids = [r.get("requirement_id") for r in req_results if isinstance(r, dict)]
    if len(rr_ids) != len(set(rr_ids)):
        errors.append("duplicate requirement_id in requirement_results")
    allowed_results = {"SATISFIED", "PARTIALLY_SATISFIED", "NOT_SATISFIED", "INSUFFICIENT_EVIDENCE", "NOT_APPLICABLE"}
    req_catalog = {r["requirement_id"]: r for r in load_yaml(ROOT / "spec" / "requirements.yaml")["requirements"]}
    for rr in req_results:
        if not isinstance(rr, dict):
            errors.append("requirement_results entries must be objects")
            continue
        rid = rr.get("requirement_id")
        meta = req_catalog.get(rid)
        if rid not in canonical_reqs:
            errors.append(f"unknown requirement_id {rid}")
        if rr.get("result") not in allowed_results:
            errors.append(f"{rid} has invalid requirement result")
        refs = rr.get("evidence_refs", []) or []
        for ref in refs:
            if ref not in evidence_ids:
                errors.append(f"{rid} references unknown evidence {ref}")
        if meta and meta.get("capability_id") and meta.get("capability_id") not in set(cap_ids):
            errors.append(f"{rid} belongs to capability {meta.get('capability_id')} outside fixture scope")
        if meta and rr.get("result") == "SATISFIED" and meta.get("normative_level") in {"SHALL","SHALL_NOT"} and not refs:
            errors.append(f"{rid} SATISFIED SHALL/SHALL_NOT requires evidence_refs")
        if rr.get("result") == "NOT_APPLICABLE" and not str(rr.get("applicability_rationale", "")).strip():
            errors.append(f"{rid} NOT_APPLICABLE requires applicability_rationale")

    gate_spec = load_yaml(ROOT / "spec" / "gates.yaml")
    known_gate_ids = {g["gate_id"] for fam in gate_spec.get("families", []) for g in fam.get("gates", [])}
    allowed_gate_inputs = {True, False, "PASS", "BREACH", "INCOMPLETE", "NOT_APPLICABLE"}
    for gid, val in (fixture.get("gate_inputs", {}) or {}).items():
        if gid not in known_gate_ids:
            errors.append(f"unknown gate_inputs gate_id {gid}")
        if val not in allowed_gate_inputs:
            errors.append(f"gate_inputs.{gid} has invalid value")

    for collection_name in ("agent_events", "decision_events"):
        for ev in fixture.get(collection_name, []) or []:
            ts = ev.get("occurred_at") if isinstance(ev, dict) else None
            if ts:
                try:
                    ev_dt = _parse_timestamp(ts)
                    if cutoff and ev_dt > _parse_timestamp(cutoff):
                        errors.append(f"{collection_name}.{ev.get('event_id','?')} occurs after evidence cutoff")
                except (TypeError, ValueError):
                    errors.append(f"{collection_name}.{ev.get('event_id','?')} has invalid occurred_at")
    return errors


def _canonical_dimension_index() -> dict[str, str]:
    return {c["capability_id"]: c["dimension_code"] for c in load_yaml(ROOT / "spec" / "capabilities.yaml")["capabilities"]}


def _critical_capability_ids() -> set[str]:
    return {
        r["capability_id"]
        for r in load_yaml(ROOT / "spec" / "requirements.yaml")["requirements"]
        if r.get("capability_id") and r.get("criticality") == "critical" and r.get("normative_level") in {"SHALL", "SHALL_NOT"}
    }


def _band_for_index(value: float | None) -> str | None:
    if value is None:
        return None
    if value < 1.8:
        return "Initial"
    if value < 2.6:
        return "Emerging"
    if value < 3.4:
        return "Defined"
    if value < 4.2:
        return "Managed"
    return "Adaptive"


def aggregation_summary(assessment_type: str, capability_results: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply EAIMS FULL/PARTIAL/TARGETED reporting semantics without hidden weighting."""
    dim_index = _canonical_dimension_index()
    by_dim: dict[str, list[dict[str, Any]]] = {}
    for r in capability_results:
        by_dim.setdefault(dim_index.get(r["capability_id"], "UNKNOWN"), []).append(r)
    dimension_profile = {
        d: geometric_index(rows) for d, rows in sorted(by_dim.items()) if d != "UNKNOWN"
    }
    determinate = [r for r in capability_results if r.get("result") in LEVEL_NUM]
    applicable = [r for r in capability_results if r.get("result") != "NOT_APPLICABLE"]
    assessed = [r for r in capability_results if r.get("result") != "NOT_ASSESSED"]
    applicable_determinate = len(determinate) / len(applicable) if applicable else 0.0
    critical = _critical_capability_ids()
    result_ids = {r["capability_id"]: r.get("result") for r in capability_results}
    critical_assessed = all(result_ids.get(cid) not in {None, "NOT_ASSESSED"} for cid in critical)
    dimensions_represented = len({dim_index.get(r["capability_id"]) for r in assessed if dim_index.get(r["capability_id"])})
    coverage = {
        "capabilities_in_scope": len(capability_results),
        "applicable_capabilities": len(applicable),
        "determinate_capabilities": len(determinate),
        "applicable_determinate_ratio": round(applicable_determinate, 4),
        "critical_capabilities_assessed": critical_assessed,
        "dimensions_represented": dimensions_represented,
    }
    scoped = geometric_index(capability_results)
    out: dict[str, Any] = {"dimension_profile": dimension_profile, "coverage": coverage}
    if assessment_type == "TARGETED":
        out.update({"indicative_scoped_index": None, "enterprise_index": None, "enterprise_maturity_established": False, "enterprise_band": None})
    elif assessment_type == "PARTIAL":
        out.update({"indicative_scoped_index": scoped, "enterprise_index": None, "enterprise_maturity_established": False, "enterprise_band": None})
    else:
        established = bool(critical_assessed and applicable_determinate >= 0.80 and dimensions_represented == 8)
        out.update({
            "indicative_scoped_index": scoped if not established else None,
            "enterprise_index": scoped if established else None,
            "enterprise_maturity_established": established,
            "enterprise_band": _band_for_index(scoped) if established else None,
        })
    return out

def assess_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    fixture_errors = validate_fixture(fixture)
    if fixture_errors:
        raise ValueError("Invalid EAIMS fixture: " + "; ".join(fixture_errors))
    cutoff=fixture["assessment"]["evidence_cutoff_time"]
    evidence=fixture.get("evidence",[])
    evidence_errors={e["evidence_id"]:validate_evidence(e,cutoff) for e in evidence}
    evidence_errors={k:v for k,v in evidence_errors.items() if v}
    req_catalog={r["requirement_id"]:r for r in load_yaml(ROOT/"spec"/"requirements.yaml")["requirements"]}
    req_results=[]
    for rr in fixture.get("requirement_results",[]):
        base=req_catalog.get(rr["requirement_id"],{})
        req_results.append({**rr,"criticality":base.get("criticality","normal"),"normative_level":base.get("normative_level"),"capability_id":base.get("capability_id")})
    by_cap={}
    for rr in req_results:
        by_cap.setdefault(rr.get("capability_id"),[]).append(rr)
    cap_results=[]
    for c in fixture.get("capabilities",[]):
        cap_results.append(award_capability(c,by_cap.get(c["capability_id"],[]),evidence))
    cap_results,dependency_findings=apply_cross_capability_dependencies(cap_results,fixture.get("capabilities",[]),fixture.get("system",{}))
    risk=derive_risk(fixture["risk_profile"])
    permission_eval=evaluate_permission_envelope(fixture["system"],fixture.get("permission_envelope"),fixture.get("agent_events",[]))
    auto_agent_gate_inputs=automated_agent_gate_inputs(fixture["system"],fixture.get("permission_envelope"),fixture.get("agent_events",[]),fixture.get("agent_controls",{}))
    hab_eval=evaluate_hab_controls(fixture["system"],fixture.get("decision_policy"),fixture.get("decision_events",[]),fixture.get("high_impact_controls",{}))
    auto_high_impact_gate_inputs=automated_high_impact_gate_inputs(fixture["system"],hab_eval,fixture.get("high_impact_controls",{}))
    # Explicit evidence-backed fixture assertions may cover human-assessed gates; machine-derived
    # checks take precedence for G2/G3 controls so a fixture cannot manually hide observed violations.
    merged_gate_inputs={**fixture.get("gate_inputs",{}),**auto_agent_gate_inputs,**auto_high_impact_gate_inputs}
    gates=evaluate_gates(fixture["system"],risk,merged_gate_inputs)
    consistency=consistency_findings(fixture.get("consistency_context",{}))
    consistency.extend(dependency_findings)
    for v in permission_eval.get("violations",[]):
        consistency.append({"rule_id":"CONS-APE-001","severity":v.get("severity","MATERIAL"),"message":f"Agent permission-envelope violation: {v['type']}","event_id":v.get("event_id")})
    for v in hab_eval.get("violations",[]):
        consistency.append({"rule_id":"CONS-HAB-EXEC-001","severity":v.get("severity","MATERIAL"),"message":f"Human Accountability Boundary violation: {v['type']}","event_id":v.get("event_id")})
    autonomy_debt=derive_autonomy_debt(fixture["system"],cap_results,gates,permission_eval)
    aggregation=aggregation_summary(fixture["assessment"]["assessment_type"], cap_results)
    result={
        "assessment_id":fixture["assessment"]["assessment_id"],
        "spec_version":load_yaml(ROOT/"spec"/"core.yaml").get("spec_version","1.0.0-fc16"),
        "assessment_type":fixture["assessment"]["assessment_type"],
        "evidence_cutoff_time":cutoff,
        "system":fixture["system"],
        "risk_profile":risk,
        "capability_results":cap_results,
        "requirement_results":req_results,
        "gate_results":gates,
        "permission_envelope_evaluation":permission_eval,
        "hab_evaluation":hab_eval,
        "autonomy_debt":autonomy_debt,
        "consistency_findings":consistency,
        "evidence_validation_errors":evidence_errors,
        "dimension_profile":aggregation["dimension_profile"],
        "coverage":aggregation["coverage"],
        "indicative_scoped_index":aggregation["indicative_scoped_index"],
        "enterprise_index":aggregation["enterprise_index"],
        "enterprise_maturity_established":aggregation["enterprise_maturity_established"],
        "enterprise_band":aggregation["enterprise_band"],
    }
    result["result_hash"]=content_hash(result)
    return result
