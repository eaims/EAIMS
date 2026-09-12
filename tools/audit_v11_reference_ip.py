#!/usr/bin/env python3
"""Reference/IP hygiene audit for the EAIMS 1.1 adversarial/agentic draft.

This is a repository hygiene check, not a legal opinion.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = (
    ROOT / "rfcs" / "0004-adversarial-agentic-governance.md",
    ROOT / "docs" / "ADVERSARIAL-AGENTIC-CROSSWALK-1.1-DRAFT.md",
    ROOT / "spec" / "adversarial-agentic-1.1-draft.yaml",
    ROOT / "review" / "RELEASE-READINESS-AUDIT-1.1-DRAFT.md",
)

PROHIBITED_CLAIMS = (
    "certified by nist",
    "certified by owasp",
    "certified by mitre",
    "approved by nist",
    "approved by owasp",
    "approved by mitre",
    "endorsed by nist",
    "endorsed by owasp",
    "endorsed by mitre",
    "officially equivalent to nist",
    "officially equivalent to owasp",
    "officially equivalent to mitre",
)

BOUNDARY_TERMS = (
    "non-normative",
    "does not establish certification",
    "does not reproduce protected standards text",
    "referenced rather than duplicated",
    "does not imply endorsement",
    "will not imply endorsement",
    "conceptual",
)

ORG_NAMES = ("NIST", "OWASP", "MITRE", "Anthropic", "Google Threat Intelligence Group")
LONG_QUOTE_LINE_RE = re.compile(r'^[^\n]*["“]([^"”\n]{180,})[”"][^\n]*$', re.MULTILINE)


class HygieneError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise HygieneError(message)


def audit() -> list[str]:
    messages = []
    combined = "\n".join(path.read_text(encoding="utf-8") for path in FILES)
    lower = combined.lower()

    for claim in PROHIBITED_CLAIMS:
        require(claim not in lower, f"prohibited endorsement/equivalence claim found: {claim}")

    for org in ORG_NAMES:
        require(org.lower() in lower, f"expected public reference missing: {org}")

    boundary_hits = sum(1 for term in BOUNDARY_TERMS if term.lower() in lower)
    require(boundary_hits >= 3, "insufficient reference-boundary language across candidate package")

    for path in FILES[:2]:
        text = path.read_text(encoding="utf-8")
        require(
            not LONG_QUOTE_LINE_RE.findall(text),
            f"{path.name}: possible long quoted reproduction detected",
        )

    require("clause-by-clause equivalent" not in lower, "unsupported clause-level equivalence claim detected")
    require("formal equivalence" not in lower, "unsupported formal-equivalence claim detected")

    messages.append("endorsement/equivalence claims: PASS")
    messages.append("public-source attribution presence: PASS")
    messages.append("reference-boundary language: PASS")
    messages.append("long-quote heuristic: PASS")
    return messages


def main() -> int:
    try:
        messages = audit()
    except HygieneError as exc:
        print(f"EAIMS 1.1 reference/IP hygiene audit FAILED: {exc}", file=sys.stderr)
        return 1

    print("EAIMS 1.1 reference/IP hygiene audit PASS")
    for message in messages:
        print(f"- {message}")
    print("- note: this is a repository hygiene check, not a legal opinion")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
