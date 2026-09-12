#!/usr/bin/env python3
"""EAIMS 1.1 candidate release-readiness audit.

This audit is intentionally stricter than ordinary draft validation. It checks that the
candidate package is coherent, non-normative, backwards-compatible in structure, and
free of obvious reference/versioning defects before candidate-freeze review.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

CANDIDATE = ROOT / "spec" / "adversarial-agentic-normative-candidate-1.1.yaml"
PROJECTION = ROOT / "spec" / "adversarial-agentic-candidate-projection-1.1.yaml"
PACKAGE = ROOT / "spec" / "adversarial-agentic-package-1.1-draft.yaml"
BASE_REQ = ROOT / "spec" / "requirements.yaml"
BASE_GATES = ROOT / "spec" / "gates.yaml"
BASE_ANCHORS = ROOT / "spec" / "anchor-eligibility.yaml"
MIGRATION = ROOT / "MIGRATION-v1.0-to-v1.1-DRAFT.md"
RELEASE_NOTES = ROOT / "RELEASE-NOTES-v1.1-DRAFT.md"
READINESS = ROOT / "FINAL-READINESS-v1.1-DRAFT.md"
RFC = ROOT / "rfcs" / "0004-adversarial-agentic-governance.md"

ALLOWED_GATE_EFFECTS = {
    "critical_risk_flag",
    "maturity_cap",
    "scale_block",
    "deployment_block",
    "mandatory_remediation",
    "reassessment_required",
}

URL_RE = re.compile(r"https://[^\s)>]+")


class AuditError(Exception):
    pass


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def collect_manifest_paths(node: Any) -> list[str]:
    if isinstance(node, str):
        if "/" in node or node.endswith((".md", ".yaml", ".py")):
            return [node]
        return []
    if isinstance(node, list):
        out: list[str] = []
        for item in node:
            out.extend(collect_manifest_paths(item))
        return out
    if isinstance(node, dict):
        out: list[str] = []
        for value in node.values():
            out.extend(collect_manifest_paths(value))
        return out
    return []


def audit() -> list[str]:
    messages: list[str] = []

    candidate = load_yaml(CANDIDATE)
    projection = load_yaml(PROJECTION)
    package = load_yaml(PACKAGE)
    base_req = load_yaml(BASE_REQ)
    base_gates = load_yaml(BASE_GATES)
    base_anchors = load_yaml(BASE_ANCHORS)

    base_requirements = base_req.get("requirements", base_req)
    base_ids = {r["requirement_id"] for r in base_requirements}
    base_cap_ids = {c["capability_id"] for c in base_anchors["capabilities"]}
    base_gate_ids = {
        gate["gate_id"]
        for family in base_gates["families"]
        for gate in family["gates"]
    }

    # Version and non-normative hygiene.
    require(candidate["target_version"] == 1.1, "candidate target_version must be 1.1")
    require(projection["target_version"] == 1.1, "projection target_version must be 1.1")
    require(candidate.get("normative") is False, "candidate must remain non-normative before freeze")
    require(projection.get("normative") is False, "projection must remain non-normative before freeze")
    require(package.get("normative") is False, "package manifest must remain non-normative")
    messages.append("version/non-normative hygiene: PASS")

    # New and amended requirement integrity.
    new = candidate["new_requirements"]
    new_ids = {r["requirement_id"] for r in new}
    require(len(new_ids) == len(new), "duplicate new requirement IDs")
    require(not (new_ids & base_ids), "new 1.1 IDs collide with EAIMS 1.0 requirement IDs")
    require("EAIMS-ADV-009" not in new_ids, "ADV-009 must not be a final candidate requirement")
    require(new_ids == set(projection["new_requirement_ids"]), "candidate/projection new requirement mismatch")

    for req in new:
        require(req["capability_id"] in base_cap_ids, f"{req['requirement_id']}: unknown capability")
        require(req["normative_level"] in {"SHALL","SHALL_NOT","SHOULD","SHOULD_NOT","MAY"}, f"{req['requirement_id']}: invalid normative level")
        require(req["machine_verifiability"] in {"MV1","MV2","MV3","MV4"}, f"{req['requirement_id']}: invalid machine-verifiability")
        require(bool(req["statement"].strip()), f"{req['requirement_id']}: empty statement")

    amended = candidate["amended_existing_requirements"]
    require(set(amended) == {"EAIMS-MSP-005","EAIMS-MSP-008"}, "unexpected amended requirement set")
    require(set(amended).issubset(base_ids), "amended IDs must exist in 1.0")
    messages.append("requirement IDs/capabilities: PASS")

    # Candidate gate integrity and collision check.
    candidate_gates = candidate["candidate_gate_extensions"]["G3"]
    candidate_gate_ids = {g["gate_id"] for g in candidate_gates}
    require(candidate_gate_ids == {"G3-13","G3-14","G3-15","G3-16","G3-17"}, "unexpected candidate G3 extension set")
    require(not (candidate_gate_ids & base_gate_ids), "candidate G3 gate IDs collide with 1.0 gate IDs")
    for gate in candidate_gates:
        require(set(gate["requirement_ids"]).issubset(new_ids), f"{gate['gate_id']}: orphan requirement reference")
    messages.append("candidate gate references: PASS")

    # Projection must not activate development-only ADV-009.
    require(projection["development_only_ids"] == ["EAIMS-ADV-009"], "ADV-009 development trace mismatch")
    active_projection_ids = set(projection["activation_projection"])
    require("EAIMS-ADV-009" not in active_projection_ids, "ADV-009 leaked into active candidate projection")
    require(set(projection["amended_existing_requirement_ids"]) == set(amended), "projection amended-ID mismatch")
    messages.append("candidate projection/consolidation: PASS")

    # Package manifest completeness.
    package_paths = collect_manifest_paths({
        k: v for k, v in package.items()
        if k not in {"profile_id","status","normative","target_version","package_rules"}
    })
    missing = [p for p in package_paths if not (ROOT / p).exists()]
    require(not missing, f"package manifest missing paths: {missing}")
    require(len(package_paths) == len(set(package_paths)), "package manifest contains duplicate path entries")
    messages.append(f"package manifest paths: PASS ({len(package_paths)})")

    # Backward-compatibility guarantees must be explicit.
    migration_text = MIGRATION.read_text(encoding="utf-8")
    release_text = RELEASE_NOTES.read_text(encoding="utf-8")
    readiness_text = READINESS.read_text(encoding="utf-8")
    require("historical 1.0.x" in migration_text.lower() or "1.0.x assessment remains" in migration_text.lower(), "migration guide lacks historical 1.0.x preservation statement")
    require("1.0.x assessments remain valid" in release_text, "release notes lack 1.0.x validity statement")
    require("NOT READY FOR NORMATIVE FREEZE" in readiness_text, "readiness status must remain pre-freeze")
    messages.append("backward compatibility/release labeling: PASS")

    # RFC/reference hygiene: references are conceptual, not endorsement/equivalence.
    rfc_text = RFC.read_text(encoding="utf-8")
    required_phrases = [
        "does not become a penetration-testing standard",
        "referenced rather than duplicated",
        "does not imply endorsement",
    ]
    for phrase in required_phrases:
        require(phrase.lower() in rfc_text.lower(), f"RFC missing reference-boundary phrase: {phrase}")

    urls = set(URL_RE.findall(rfc_text))
    require(any("nist.gov" in u for u in urls), "RFC missing NIST public reference")
    require(any("owasp" in u for u in urls), "RFC missing OWASP public reference")
    require(any("mitre" in u for u in urls), "RFC missing MITRE public reference")
    require(any("anthropic.com" in u for u in urls), "RFC missing Anthropic threat-intelligence reference")
    messages.append("reference/IP boundary hygiene: PASS")

    # Ensure candidate package is additive and does not rewrite canonical 1.0 version labels.
    require(base_req["spec_version"].startswith("1.0.0"), "base requirements version unexpectedly changed")
    require(base_gates["spec_version"].startswith("1.0.0"), "base gates version unexpectedly changed")
    require(base_anchors["spec_version"].startswith("1.0.0"), "base anchor version unexpectedly changed")
    messages.append("canonical 1.0 baseline preservation: PASS")

    return messages


def main() -> int:
    try:
        messages = audit()
    except (AuditError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f"EAIMS 1.1 release-readiness audit FAILED: {exc}", file=sys.stderr)
        return 1

    print("EAIMS 1.1 release-readiness audit PASS")
    for message in messages:
        print(f"- {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
