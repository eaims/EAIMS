#!/usr/bin/env python3
"""Build the CSV, JSON, and Markdown questionnaires from the capability matrix."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "Capability-Matrix-v0.2.md"
OUT = ROOT / "assessment"

text = MATRIX.read_text(encoding="utf-8")
dimension = ""
capabilities = []
for line in text.splitlines():
    dim = re.match(r"^## (\d+)\. (.+)$", line)
    if dim:
        dimension_id, dimension = dim.groups()
        continue
    cap = re.match(r"^### (\d+\.\d+) (.+)$", line)
    if not cap:
        continue
    capability_id, capability = cap.groups()
    start = text.index(line) + len(line)
    next_heading = text.find("\n### ", start)
    next_dimension = text.find("\n## ", start)
    ends = [p for p in (next_heading, next_dimension) if p >= 0]
    block = text[start:min(ends) if ends else len(text)]
    levels = {}
    for row in block.splitlines():
        match = re.match(r"\| ([0-5]) \| (.+) \|$", row)
        if match:
            levels[int(match.group(1))] = match.group(2)
    if set(levels) != set(range(6)):
        raise ValueError(f"{capability_id} must define levels 0 through 5")
    capabilities.append({
        "dimension_id": dimension_id,
        "dimension": dimension,
        "capability_id": capability_id,
        "capability": capability,
        "levels": levels,
    })

critical_dimensions = {"3", "6", "7"}
questions = []
for index, item in enumerate(capabilities, 1):
    questions.append({
        "question_id": f"Q{index:03d}",
        **item,
        "question": f"Which statement best describes the organization's current capability for {item['capability']}?",
        "response_type": "single_select_0_to_5",
        "required_evidence": "Document, metric, observation, interview, or system record",
        "critical": item["dimension_id"] in critical_dimensions,
    })

payload = {"standard": "EAIMS", "version": "0.2.1", "status": "community-draft", "questions": questions}
(OUT / "questionnaire.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

fields = ["question_id", "dimension_id", "dimension", "capability_id", "capability", "question",
          "response_type", "required_evidence", "critical", *[f"level_{n}" for n in range(6)]]
with (OUT / "questionnaire.csv").open("w", encoding="utf-8-sig", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    for q in questions:
        row = {k: q[k] for k in fields if k in q}
        row["critical"] = "yes" if q["critical"] else "no"
        row.update({f"level_{n}": q["levels"][n] for n in range(6)})
        writer.writerow(row)

md = ["# EAIMS Assessment Questionnaire", "", "> Select the highest level fully supported by evidence. If evidence is incomplete, choose the lower defensible level.", ""]
for q in questions:
    md += [f"## {q['question_id']} — {q['capability']}", "", f"**Dimension:** {q['dimension']}  ",
           f"**Critical gate:** {'Yes' if q['critical'] else 'No'}", "", q["question"], "",
           "| Score | Observable maturity anchor |", "|---:|---|"]
    md += [f"| {n} | {q['levels'][n]} |" for n in range(6)]
    md += ["", "**Selected score:**  ", "**Evidence IDs:**  ", "**Confidence (low / medium / high):**  ", "**Assessor notes:**", ""]
(OUT / "questionnaire.md").write_text("\n".join(md), encoding="utf-8")

print(f"Built three questionnaire formats from {len(questions)} capabilities")
