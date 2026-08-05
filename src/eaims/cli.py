"""EAIMS command-line interface."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .reporting import html_report, markdown_report
from .scoring import AssessmentError, score_assessment, validate_assessment


def _load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eaims", description="EAIMS reference assessment engine")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "score"):
        p = sub.add_parser(name)
        p.add_argument("assessment")
    report = sub.add_parser("report")
    report.add_argument("assessment")
    report.add_argument("--format", choices=("markdown", "html"), default="markdown")
    report.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        data = _load(args.assessment)
        if args.command == "validate":
            errors = validate_assessment(data)
            if errors:
                print("\n".join(errors), file=sys.stderr)
                return 1
            print("valid")
            return 0
        result = score_assessment(data)
        if args.command == "score":
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 0
        rendered = html_report(result) if args.format == "html" else markdown_report(result)
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            print(rendered)
        return 0
    except (OSError, json.JSONDecodeError, AssessmentError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
