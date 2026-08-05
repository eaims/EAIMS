#!/usr/bin/env python3
"""Build evidence catalog and complete fictional assessments."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
questions = json.loads((ROOT / "assessment/questionnaire.json").read_text(encoding="utf-8"))["questions"]

evidence = {
"1.1":["approved AI strategy", "strategy-to-outcome map", "funded transformation roadmap"],
"1.2":["executive accountability charter", "governance meeting decisions", "portfolio escalation records"],
"1.3":["AI policy set", "decision-right matrix", "policy exception register"],
"2.1":["use-case inventory", "prioritization criteria", "portfolio decision records"],
"2.2":["approved business cases", "benefit baselines", "benefits-realization reviews"],
"2.3":["AI budget model", "capacity plan", "unit-cost or FinOps dashboard"],
"3.1":["data-owner register", "catalog and lineage records", "stewardship performance reports"],
"3.2":["data-quality rules", "quality service levels", "remediation and outcome records"],
"3.3":["content inventory", "permission and retention controls", "retrieval-quality evaluation"],
"4.1":["AI reference architecture", "approved engineering patterns", "architecture review decisions"],
"4.2":["engineering lifecycle standard", "test and review records", "reusable component catalog"],
"4.3":["RAG or agent design pattern", "prompt and tool evaluation records", "agent permission controls"],
"5.1":["capacity and deployment architecture", "performance and cost records", "resilience test results"],
"5.2":["platform service catalog", "self-service guardrails", "golden-path adoption metrics"],
"5.3":["service objectives", "dependency and recovery plan", "tested failover evidence"],
"6.1":["version-controlled pipelines", "approval and rollback records", "deployment policy tests"],
"6.2":["evaluation standard", "pre-production results", "production quality and risk monitoring"],
"6.3":["AI incident procedure", "change and retirement records", "post-incident learning actions"],
"7.1":["AI system inventory", "risk-tier methodology", "risk register and control reviews"],
"7.2":["AI threat models", "access and logging evidence", "supplier and dependency assurance"],
"7.3":["impact assessment", "human-oversight design", "fairness, transparency, and safety reviews"],
"8.1":["AI skills taxonomy", "role-based learning records", "workforce capability plan"],
"8.2":["AI operating model", "cross-functional responsibility matrix", "delivery performance reviews"],
"8.3":["safe-experimentation policy", "incentive design", "culture and trust measurements"],
"9.1":["current and target process maps", "human-AI control design", "process outcome measures"],
"9.2":["stakeholder and adoption plan", "training and support records", "usage and behavior metrics"],
"9.3":["balanced KPI definition", "baseline and outcome dashboard", "portfolio optimization decisions"],
}

catalog = {"standard":"EAIMS", "version":"0.2.0", "status":"community-draft", "capabilities":[]}
for q in questions:
    cid = q["capability_id"]
    catalog["capabilities"].append({
        "capability_id": cid, "capability": q["capability"], "dimension": q["dimension"],
        "evidence_examples": evidence[cid],
        "level_3_minimum": [evidence[cid][0], evidence[cid][1]],
        "level_4_expectation": "Evidence is measured over time and informs documented improvement.",
        "level_5_expectation": "Evidence demonstrates continuous adaptation within governed boundaries.",
        "counter_evidence": ["policy exists but is not used", "claims rely only on interviews", "evidence is stale or outside assessment scope"],
        "freshness_guidance_months": 12,
    })
(ROOT / "assessment/evidence-catalog.json").write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")

profiles = {
    "fictional-manufacturer": [3,2,2,2,2,2,2,2,2],
    "fictional-bank": [4,3,4,3,3,3,4,3,3],
    "fictional-cloud-company": [4,4,4,4,4,4,3,4,4],
}
for slug, dims in profiles.items():
    rows=[]
    for d, base in enumerate(dims,1):
        for c in range(1,4):
            score=max(0,min(5,base + (1 if c==1 else 0) - (1 if c==3 else 0)))
            rows.append({"capability_id":f"{d}.{c}","score":score,"confidence":"high" if d%3 else "medium",
                         "evidence_ids":[f"EV-{d}{c}-01"] if score>=3 else [],"notes":"Fictional training example."})
    item={"standard":"EAIMS","version":"0.2.0","organization":slug.replace("-"," ").title(),
          "assessment_date":"2026-08-03","assessment_type":"facilitated","scope":"Fictional enterprise-wide example",
          "capability_scores":rows}
    (ROOT / f"examples/{slug}.assessment.json").write_text(json.dumps(item,indent=2)+"\n",encoding="utf-8")
print("Built evidence catalog and three fictional assessments")
