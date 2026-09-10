from pathlib import Path
from .paths import ROOT
import json, yaml


def load_yaml(name):
    with open(ROOT / "spec" / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_referential_integrity():
    caps = load_yaml("capabilities.yaml")
    reqs = load_yaml("requirements.yaml")
    gates = load_yaml("gates.yaml")
    anchor_elig = load_yaml("anchor-eligibility.yaml")
    machine = load_yaml("machine-verification.yaml")
    consistency = load_yaml("consistency.yaml")
    tests = yaml.safe_load((ROOT / "tests" / "catalog.yaml").read_text(encoding="utf-8"))

    errors=[]
    cap_ids=[c["capability_id"] for c in caps.get("capabilities",[])]
    req_ids=[r["requirement_id"] for r in reqs.get("requirements",[])]
    if len(cap_ids)!=30: errors.append(f"expected 30 capabilities, found {len(cap_ids)}")
    if len(cap_ids)!=len(set(cap_ids)): errors.append("duplicate capability_id")
    if len(req_ids)!=len(set(req_ids)): errors.append("duplicate requirement_id")
    valid_caps=set(cap_ids); valid_reqs=set(req_ids)

    canonical_levels={"L1","L2","L3","L4","L5"}
    for c in caps.get("capabilities",[]):
        anchors=c.get("anchors",{})
        if set(anchors)!=canonical_levels:
            errors.append(f"{c['capability_id']} missing canonical L1-L5 anchors")
        if not c.get("dimension_code"):
            errors.append(f"{c['capability_id']} missing dimension_code")

    cap_req_counts={c:0 for c in cap_ids}
    for r in reqs.get("requirements",[]):
        rid=r.get("requirement_id")
        cid=r.get("capability_id")
        if cid:
            if cid not in valid_caps: errors.append(f"unknown capability_id {cid} in {rid}")
            else: cap_req_counts[cid]+=1
        if r.get("normative_level") not in {"SHALL","SHALL_NOT","SHOULD","SHOULD_NOT","MAY"}:
            errors.append(f"invalid normative_level in {rid}")
        if r.get("machine_verifiability") not in {"MV1","MV2","MV3","MV4"}:
            errors.append(f"invalid machine_verifiability in {rid}")
        if r.get("criticality") not in {"normal","material","critical"}:
            errors.append(f"invalid criticality in {rid}")
        if not str(r.get("statement","")).strip():
            errors.append(f"empty statement in {rid}")
    for cid,n in cap_req_counts.items():
        if n<4: errors.append(f"{cid} has only {n} capability requirements")

    # Gate integrity: gates are nested under families.
    gate_ids=[]
    for family in gates.get("families",[]):
        fid=family.get("family")
        if fid not in {"G0","G1","G2","G3"}:
            errors.append(f"unknown gate family {fid}")
        for g in family.get("gates",[]):
            gid=g.get("gate_id"); gate_ids.append(gid)
            refs=[]
            if g.get("requirement_id"): refs.append(g["requirement_id"])
            refs += g.get("requirement_ids",[]) or []
            if not refs: errors.append(f"gate {gid} has no requirement reference")
            for rid in refs:
                if rid not in valid_reqs: errors.append(f"gate {gid} references unknown requirement {rid}")
    if len(gate_ids)!=len(set(gate_ids)): errors.append("duplicate gate_id")

    # Capability-specific anchor eligibility integrity and exact anchor text synchronization.
    ae_caps=anchor_elig.get("capabilities",[])
    if len(ae_caps)!=30: errors.append(f"expected 30 anchor-eligibility capability records, found {len(ae_caps)}")
    ae_ids=[c.get("capability_id") for c in ae_caps]
    if len(ae_ids)!=len(set(ae_ids)): errors.append("duplicate anchor-eligibility capability_id")
    if set(ae_ids)!=valid_caps: errors.append("anchor-eligibility capability set differs from canonical capability set")
    canonical_by={c["capability_id"]:c for c in caps.get("capabilities",[])}
    req_by={r["requirement_id"]:r for r in reqs.get("requirements",[])}
    for c in ae_caps:
        cid=c.get("capability_id")
        if set(c.get("levels",{}))!=canonical_levels:
            errors.append(f"{cid} missing L1-L5 eligibility rules")
        if cid in canonical_by and c.get("anchor_statement_refs",{}) != canonical_by[cid].get("anchors",{}):
            errors.append(f"{cid} anchor_statement_refs drift from canonical capability anchors")
        for lvl,rule in c.get("levels",{}).items():
            if rule.get("minimum_evidence_class") not in {None,"E1","E2","E3","E4"}:
                errors.append(f"{cid} {lvl} has invalid minimum_evidence_class")
            for rid in rule.get("required_requirements",[]) or []:
                if rid not in valid_reqs:
                    errors.append(f"anchor eligibility {cid} {lvl} references unknown requirement {rid}")
                elif req_by[rid].get("capability_id") not in {cid,None}:
                    errors.append(f"anchor eligibility {cid} {lvl} references requirement {rid} owned by another capability")
    dep_ids=[]
    for d in anchor_elig.get("dependencies",[]) or []:
        dep_ids.append(d.get("rule_id"))
        if d.get("capability_id") not in valid_caps or d.get("dependency_capability") not in valid_caps:
            errors.append(f"dependency {d.get('rule_id')} references unknown capability")
        if d.get("target_level") not in canonical_levels or d.get("minimum_level") not in canonical_levels:
            errors.append(f"dependency {d.get('rule_id')} has invalid maturity level")
        if d.get("type") not in {"hard","supporting"}:
            errors.append(f"dependency {d.get('rule_id')} has invalid dependency type")
    if len(dep_ids)!=len(set(dep_ids)): errors.append("duplicate dependency rule_id")

    # Critical machine verification rules must point to known critical MV1/MV2 normative requirements.
    mv_ids=[]
    for rule in machine.get("rules",[]):
        rid=rule.get("requirement_id"); mv_ids.append(rid)
        if rid not in valid_reqs:
            errors.append(f"machine verification references unknown requirement {rid}")
            continue
        r=req_by[rid]
        if r.get("machine_verifiability") not in {"MV1","MV2"}:
            errors.append(f"machine verification rule {rid} is not MV1/MV2")
        if r.get("criticality") != "critical" or r.get("normative_level") not in {"SHALL","SHALL_NOT"}:
            errors.append(f"machine verification rule {rid} is not a critical SHALL/SHALL_NOT")
    if len(mv_ids)!=len(set(mv_ids)): errors.append("duplicate machine-verification requirement_id")

    # Consistency rule IDs are stable and unique.
    cons_rules=consistency.get("rules",[]) or []
    cons_ids=[r.get("rule_id") for r in cons_rules]
    if len(cons_ids)!=len(set(cons_ids)): errors.append("duplicate consistency rule_id")

    aq=load_yaml("assessment-quality.yaml")
    if set(aq.get("quality_levels",[]))!={"HIGH","MODERATE","LIMITED"}:
        errors.append("invalid assessment-quality levels")
    ma=load_yaml("multi-assessor.yaml")
    required_resolution={"requirement_id","resolver_id","final_decision","rationale","evidence_refs","considered_assessor_ids","resolved_at"}
    if set(ma.get("resolution_required_fields",[]))!=required_resolution:
        errors.append("invalid multi-assessor resolution field set")

    test_ids=[t.get('test_id') for t in tests.get('tests',[])]
    if len(test_ids)!=len(set(test_ids)): errors.append('duplicate test_id')
    return errors


def summary():
    caps=load_yaml('capabilities.yaml')['capabilities']; reqs=load_yaml('requirements.yaml')['requirements']
    shall=[r for r in reqs if r['normative_level'] in ('SHALL','SHALL_NOT')]
    critical=[r for r in shall if r['criticality']=='critical']
    return {
        'capabilities':len(caps),
        'anchors':sum(len(c['anchors']) for c in caps),
        'anchor_eligibility_rules':sum(len(c.get('levels',{})) for c in load_yaml('anchor-eligibility.yaml').get('capabilities',[])),
        'requirements':len(reqs),
        'shall_requirements':len(shall),
        'critical_shall_requirements':len(critical),
    }


def main():
    errs=validate_referential_integrity()
    print(json.dumps(summary(),indent=2))
    if errs:
        print("FAIL")
        for e in errs: print("-",e)
        raise SystemExit(1)
    print("PASS: canonical specification integrity")


if __name__ == "__main__":
    main()
