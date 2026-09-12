#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "spec" / "adversarial-agentic-normative-candidate-1.1.yaml"
PROJECTION = ROOT / "spec" / "adversarial-agentic-candidate-projection-1.1.yaml"
PACKAGE = ROOT / "spec" / "adversarial-agentic-package-1.1-draft.yaml"
BASE_REQ = ROOT / "spec" / "requirements.yaml"

def fail(msg):
    print(f"EAIMS 1.1 candidate audit FAILED: {msg}", file=sys.stderr)
    raise SystemExit(1)

def _collect_paths(node):
    if isinstance(node, str):
        if "/" in node or node.endswith((".md", ".yaml", ".py")):
            return [node]
        return []
    if isinstance(node, list):
        result = []
        for item in node:
            result.extend(_collect_paths(item))
        return result
    if isinstance(node, dict):
        result = []
        for value in node.values():
            result.extend(_collect_paths(value))
        return result
    return []

def main():
    cand = yaml.safe_load(CANDIDATE.read_text(encoding="utf-8"))
    projection = yaml.safe_load(PROJECTION.read_text(encoding="utf-8"))
    package = yaml.safe_load(PACKAGE.read_text(encoding="utf-8"))
    base = yaml.safe_load(BASE_REQ.read_text(encoding="utf-8"))
    base_reqs = base.get("requirements", base)
    base_ids = {r["requirement_id"] for r in base_reqs}

    if cand.get("normative") is not False or projection.get("normative") is not False:
        fail("candidate artifacts must remain non-normative until freeze")

    new = cand["new_requirements"]
    new_ids = [r["requirement_id"] for r in new]
    if len(new_ids) != len(set(new_ids)):
        fail("duplicate new requirement IDs")
    if set(new_ids) & base_ids:
        fail("new candidate IDs collide with 1.0 IDs")
    if "EAIMS-ADV-009" in new_ids:
        fail("ADV-009 must be consolidated, not retained as a new normative candidate ID")

    amended = cand["amended_existing_requirements"]
    if set(amended) != {"EAIMS-MSP-005", "EAIMS-MSP-008"}:
        fail("unexpected amended requirement set")
    if not set(amended).issubset(base_ids):
        fail("amended requirements must exist in 1.0")

    projected_new = set(projection["new_requirement_ids"])
    if projected_new != set(new_ids):
        fail("candidate projection new requirement set does not match normative candidate overlay")
    if set(projection["amended_existing_requirement_ids"]) != set(amended):
        fail("candidate projection amended requirement set does not match normative candidate overlay")
    if "EAIMS-ADV-009" in projection["activation_projection"]:
        fail("ADV-009 must not remain active in candidate projection")
    if projection.get("development_only_ids") != ["EAIMS-ADV-009"]:
        fail("candidate projection must retain ADV-009 only as a development-only trace")

    gate_refs = {
        rid
        for gate in cand["candidate_gate_extensions"]["G3"]
        for rid in gate["requirement_ids"]
    }
    if not gate_refs.issubset(set(new_ids)):
        fail("candidate gates reference unknown/non-new ADV IDs")

    retained = set(cand["design_decisions"]["retained_new_requirements"])
    if retained != set(new_ids):
        fail("retained-new-requirement decision does not match candidate new requirements")

    merged = cand["design_decisions"]["consolidated_development_requirement"]
    if set(merged) != {"EAIMS-ADV-009"}:
        fail("expected exactly ADV-009 as consolidated development requirement")

    package_paths = _collect_paths({
        k: v for k, v in package.items()
        if k not in {"profile_id", "status", "normative", "target_version", "package_rules"}
    })
    missing = [p for p in package_paths if not (ROOT / p).exists()]
    if missing:
        fail(f"package manifest references missing paths: {missing}")

    if package["specification_overlays"].get("candidate_projection") != "spec/adversarial-agentic-candidate-projection-1.1.yaml":
        fail("package manifest must include candidate projection")

    print("EAIMS 1.1 candidate audit PASS")
    print(f"- new candidate requirements: {len(new_ids)}")
    print(f"- strengthened existing requirements: {len(amended)}")
    print(f"- candidate G3 extensions: {len(cand['candidate_gate_extensions']['G3'])}")
    print(f"- package paths checked: {len(package_paths)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
