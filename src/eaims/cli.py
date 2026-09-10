from pathlib import Path
import argparse, json, sys, yaml

from .engine import assess_fixture, validate_fixture
from .report import render_markdown
from .input_io import load_input_yaml
from .review import validate_review_record, validate_resolution_record, aggregate_findings, apply_resolutions, review_summary, render_review_markdown
from .legacy_compat import (
    LegacyAssessmentError, validate_legacy_assessment, score_legacy_assessment,
    legacy_markdown_report, legacy_html_report,
)


def _load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="eaims", description="EAIMS reference assessment engine")
    sub = p.add_subparsers(dest="cmd", required=True)

    # EAIMS 1.0 executable workflow
    a = sub.add_parser("assess", help="Run an EAIMS 1.0 YAML fixture")
    a.add_argument("fixture")
    a.add_argument("--out", default="run-output")

    fv = sub.add_parser("validate-fixture", help="Validate an EAIMS 1.0 YAML fixture without scoring")
    fv.add_argument("fixture")

    r = sub.add_parser("review")
    rsub = r.add_subparsers(dest="review_cmd", required=True)
    rv = rsub.add_parser("validate")
    rv.add_argument("record")
    rs = rsub.add_parser("summarize")
    rs.add_argument("fixture")
    rs.add_argument("--out", default="review-output")
    rs.add_argument("--fail-on-unmet", action="store_true",
                    help="Exit 1 when review exit criteria are not met; still write reports")

    # Backward-compatible v0.2.1 CLI contract already published by EAIMS.
    for name in ("validate", "score"):
        lp = sub.add_parser(name, help=f"Legacy EAIMS v0.2.1 {name} compatibility")
        lp.add_argument("assessment")
    lr = sub.add_parser("report", help="Legacy EAIMS v0.2.1 report compatibility")
    lr.add_argument("assessment")
    lr.add_argument("--format", choices=("markdown", "html"), default="markdown")
    lr.add_argument("--output")

    args = p.parse_args(argv)
    try:
        if args.cmd == "validate-fixture":
            fixture = load_input_yaml(args.fixture)
            errors = validate_fixture(fixture)
            print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
            return 0 if not errors else 1

        if args.cmd == "assess":
            fixture = load_input_yaml(args.fixture)
            errors = validate_fixture(fixture)
            if errors:
                print(json.dumps({"valid": False, "errors": errors}, ensure_ascii=False, indent=2), file=sys.stderr)
                return 1
            result = assess_fixture(fixture)
            out = Path(args.out)
            out.mkdir(parents=True, exist_ok=True)
            (out / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            (out / "report.md").write_text(render_markdown(result), encoding="utf-8")
            print(json.dumps({"assessment_id": result["assessment_id"], "result_hash": result["result_hash"], "out": str(out)}, indent=2))
            return 0

        if args.cmd == "review" and args.review_cmd == "validate":
            record = load_input_yaml(args.record)
            errors = validate_review_record(record)
            print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
            return 0 if not errors else 2

        if args.cmd == "review" and args.review_cmd == "summarize":
            data = load_input_yaml(args.fixture)
            if not isinstance(data, dict):
                raise ValueError("review fixture must be an object")
            records = data.get("reviews", [])
            if not isinstance(records, list):
                raise ValueError("reviews must be an array")
            for rec in records:
                errors = validate_review_record(rec)
                if errors:
                    print("Invalid review record: " + "; ".join(errors), file=sys.stderr)
                    return 2
            resolutions = data.get("resolutions", [])
            if not isinstance(resolutions, list):
                raise ValueError("resolutions must be an array")
            for resolution in resolutions:
                errors = validate_resolution_record(resolution)
                if errors:
                    print("Invalid resolution record: " + "; ".join(errors), file=sys.stderr)
                    return 2
            ledger = apply_resolutions(aggregate_findings(records), resolutions)
            summary = review_summary(records, ledger)
            out = Path(args.out)
            out.mkdir(parents=True, exist_ok=True)
            (out / "review-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
            (out / "findings-ledger.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
            (out / "review-summary.md").write_text(render_review_markdown(summary, ledger), encoding="utf-8")
            print(json.dumps({"status": summary["rc_gate"]["status"], "out": str(out)}, indent=2))
            return 1 if args.fail_on_unmet and not summary["rc_gate"]["review_completed_for_rc"] else 0

        # Legacy v0.2.1 compatibility path.
        data = _load_json(args.assessment)
        if args.cmd == "validate":
            errors = validate_legacy_assessment(data)
            if errors:
                print("\n".join(errors), file=sys.stderr)
                return 1
            print("valid")
            return 0
        result = score_legacy_assessment(data)
        if args.cmd == "score":
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 0
        rendered = legacy_html_report(result) if args.format == "html" else legacy_markdown_report(result)
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            print(rendered)
        return 0
    except (OSError, json.JSONDecodeError, yaml.YAMLError, LegacyAssessmentError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
