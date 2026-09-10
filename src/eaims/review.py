from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable
import json
import yaml
from jsonschema import Draft202012Validator, FormatChecker
from .paths import ROOT
from .input_io import load_input_yaml


def _root() -> Path:
    """Use the same installed specification root as the assessment engine."""
    return ROOT


def load_yaml(path: str | Path) -> Any:
    return load_input_yaml(path)


def validate_review_record(record: dict[str, Any], root: Path | None = None) -> list[str]:
    root = root or _root()
    schema = json.loads((root / "schemas" / "review-feedback.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for err in sorted(validator.iter_errors(record), key=lambda e: list(e.path)):
        path = ".".join(str(x) for x in err.path) or "$"
        errors.append(f"{path}: {err.message}")
    return errors


def validate_resolution_record(record: dict[str, Any], root: Path | None = None) -> list[str]:
    root = root or _root()
    schema = json.loads((root / "schemas" / "review-resolution.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for err in sorted(validator.iter_errors(record), key=lambda e: list(e.path)):
        path = ".".join(str(x) for x in err.path) or "$"
        errors.append(f"{path}: {err.message}")
    return errors


def _finding_key(review_id: str, finding: dict[str, Any]) -> str:
    return f"{review_id}:{finding['finding_id']}"


def aggregate_findings(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    ledger = []
    review_ids = set()
    finding_keys = set()
    for record in records:
        review_id = record["review_id"]
        if review_id in review_ids:
            raise ValueError(f"Duplicate review_id: {review_id}")
        review_ids.add(review_id)
        for finding in record.get("findings", []):
            key = _finding_key(review_id, finding)
            if key in finding_keys:
                raise ValueError(f"Duplicate finding_key: {key}")
            finding_keys.add(key)
            ledger.append({
                "finding_key": _finding_key(record["review_id"], finding),
                "review_id": record["review_id"],
                "reviewer_id": record["reviewer_id"],
                "domain": finding["domain"],
                "severity": finding["severity"],
                "title": finding["title"],
                "rationale": finding["rationale"],
                "evidence_or_reference": finding["evidence_or_reference"],
                "recommended_action": finding["recommended_action"],
                "resolution_status": "OPEN",
            })
    return ledger


def apply_resolutions(ledger: list[dict[str, Any]], resolutions: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key = {}
    for item in ledger:
        key = item["finding_key"]
        if key in by_key:
            raise ValueError(f"Duplicate finding_key: {key}")
        by_key[key] = dict(item)
    seen_resolution_ids=set()
    seen_findings=set()
    for r in resolutions:
        errors=validate_resolution_record(r)
        if errors:
            raise ValueError("Invalid resolution record: " + "; ".join(errors))
        rid=r["resolution_id"]
        if rid in seen_resolution_ids:
            raise ValueError(f"Duplicate resolution_id: {rid}")
        seen_resolution_ids.add(rid)
        key = r["finding_key"]
        if key in seen_findings:
            raise ValueError(f"Multiple resolutions supplied for finding_key: {key}")
        seen_findings.add(key)
        if key not in by_key:
            raise ValueError(f"Resolution references unknown finding_key: {key}")
        item = by_key[key]
        item["resolution_status"] = r["resolution_status"]
        item["resolution"] = r
    return list(by_key.values())

def rc_review_gate(records: list[dict[str, Any]], ledger: list[dict[str, Any]]) -> dict[str, Any]:
    independent = [r for r in records if r.get("independence_class") in {"EXTERNAL_INDEPENDENT", "INTERNAL_INDEPENDENT"}]
    open_blockers = [f for f in ledger if f["severity"] == "BLOCKER" and f["resolution_status"] != "RESOLVED"]
    unresolved_majors = [
        f for f in ledger
        if f["severity"] == "MAJOR" and f["resolution_status"] not in {"RESOLVED", "ACCEPTED_WITH_RATIONALE"}
    ]
    bad_dispositions = [r for r in records if r.get("overall_decision") == "NOT_READY_FOR_RC"]
    rereview = [r for r in records if r.get("overall_decision") == "REVISE_AND_REREVIEW"]

    completed = bool(independent) and not open_blockers and not unresolved_majors and not bad_dispositions and not rereview
    reasons = []
    if not independent:
        reasons.append("No independent review record exists.")
    if open_blockers:
        reasons.append(f"{len(open_blockers)} BLOCKER finding(s) remain unresolved.")
    if unresolved_majors:
        reasons.append(f"{len(unresolved_majors)} MAJOR finding(s) remain unresolved or unaccepted.")
    if bad_dispositions:
        reasons.append("At least one reviewer disposition is NOT_READY_FOR_RC.")
    if rereview:
        reasons.append("At least one reviewer requires revision and re-review.")

    return {
        "independent_review_records": len(independent),
        "open_blockers": len(open_blockers),
        "unresolved_majors": len(unresolved_majors),
        "not_ready_dispositions": len(bad_dispositions),
        "rereview_dispositions": len(rereview),
        "review_completed_for_rc": completed,
        "status": "RC_REVIEW_EXIT_CRITERIA_MET" if completed else "RC_REVIEW_EXIT_CRITERIA_NOT_MET",
        "reasons": reasons,
    }


def review_summary(records: list[dict[str, Any]], ledger: list[dict[str, Any]]) -> dict[str, Any]:
    severities = {k: 0 for k in ["BLOCKER", "MAJOR", "MODERATE", "MINOR", "EDITORIAL"]}
    domains: dict[str, int] = {}
    statuses: dict[str, int] = {}
    for f in ledger:
        severities[f["severity"]] = severities.get(f["severity"], 0) + 1
        domains[f["domain"]] = domains.get(f["domain"], 0) + 1
        statuses[f["resolution_status"]] = statuses.get(f["resolution_status"], 0) + 1
    return {
        "reviews": len(records),
        "findings": len(ledger),
        "findings_by_severity": severities,
        "findings_by_domain": dict(sorted(domains.items())),
        "resolution_status": dict(sorted(statuses.items())),
        "rc_gate": rc_review_gate(records, ledger),
    }


def render_review_markdown(summary: dict[str, Any], ledger: list[dict[str, Any]]) -> str:
    lines = [
        "# EAIMS 1.0 RC Review Summary",
        "",
        f"- Review records: **{summary['reviews']}**",
        f"- Findings: **{summary['findings']}**",
        f"- RC review exit status: **{summary['rc_gate']['status']}**",
        "",
        "## Findings by severity",
        "",
    ]
    for sev, count in summary["findings_by_severity"].items():
        lines.append(f"- {sev}: {count}")
    lines += ["", "## RC gate", ""]
    if summary["rc_gate"]["reasons"]:
        for reason in summary["rc_gate"]["reasons"]:
            lines.append(f"- {reason}")
    else:
        lines.append("- Exit criteria met.")
    lines += ["", "## Findings ledger", "", "| Finding | Domain | Severity | Status | Title |", "|---|---|---|---|---|"]
    for f in ledger:
        lines.append(f"| {f['finding_key']} | {f['domain']} | {f['severity']} | {f['resolution_status']} | {f['title']} |")
    lines += ["", "> Review completion is a design-review milestone; it does not establish empirical validity, certification, regulatory conformity, production validation, or inter-rater reliability.", ""]
    return "\n".join(lines)
