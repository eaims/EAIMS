#!/usr/bin/env python3
"""EAIMS v0.2 release validation."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from eaims.scoring import score_assessment  # noqa: E402

errors=[]
version=(ROOT/"VERSION").read_text(encoding="utf-8").strip()
manifest=json.loads((ROOT/"manifest.json").read_text(encoding="utf-8"))
questionnaire=json.loads((ROOT/"assessment/questionnaire.json").read_text(encoding="utf-8"))
catalog=json.loads((ROOT/"assessment/evidence-catalog.json").read_text(encoding="utf-8"))
for label,obj in (("manifest",manifest),("questionnaire",questionnaire),("evidence catalog",catalog)):
    if obj.get("version")!=version: errors.append(f"{label} version differs from VERSION")
if len(questionnaire.get("questions",[]))!=27: errors.append("questionnaire must contain 27 capabilities")
if len(catalog.get("capabilities",[]))!=27: errors.append("evidence catalog must contain 27 capabilities")
for path in ROOT.rglob("*.json"):
    try: json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
for path in sorted((ROOT/"examples").glob("*.assessment.json")):
    try: score_assessment(json.loads(path.read_text(encoding="utf-8")))
    except Exception as exc: errors.append(f"example {path.name} cannot score: {exc}")
required=["DCO.md","DISCLAIMER.md","IP_POLICY.md","ORIGIN.md","THIRD_PARTY_NOTICES.md","TRADEMARK.md","SPONSORSHIP.md","docs/Conformance.md","docs/Assessor-Handbook.md"]
for item in required:
    if not (ROOT/item).is_file(): errors.append(f"missing required file {item}")
link=re.compile(r"\[[^]]+\]\(([^)]+)\)")
for path in ROOT.rglob("*.md"):
    for target in link.findall(path.read_text(encoding="utf-8")):
        local=target.split("#",1)[0]
        if local and not local.startswith(("http://","https://","mailto:")) and not (path.parent/local).resolve().exists():
            errors.append(f"broken link in {path.relative_to(ROOT)}: {target}")
actual=sum(1 for p in ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts and not p.name.endswith(".pyc"))
if manifest.get("file_count")!=actual: errors.append(f"manifest file_count {manifest.get('file_count')} != {actual}")
if errors:
    print("Validation failed:\n"+"\n".join(f"- {e}" for e in errors)); raise SystemExit(1)
print(f"EAIMS v{version} validated: {actual} files, 27 capabilities, 3 executable examples")
