"""Human-readable report rendering."""
from __future__ import annotations

from html import escape
from typing import Any


def markdown_report(result: dict[str, Any]) -> str:
    lines = [
        f"# EAIMS Assessment — {result['organization']}", "",
        f"- **Version:** {result['version']}",
        f"- **Date:** {result['assessment_date']}",
        f"- **Type:** {result['assessment_type']}",
        f"- **Scope:** {result['scope']}",
        f"- **Aggregate score:** {result['aggregate_score']:.2f}",
        f"- **Final maturity level:** {result['final_level']}",
        f"- **Provisional:** {'Yes' if result['provisional'] else 'No'}", "",
        "## Dimension profile", "", "| Dimension | Score |", "|---|---:|",
    ]
    lines += [f"| {name} | {score:.2f} |" for name, score in result["dimension_scores"].items()]
    lines += ["", "## Gate adjustments", ""]
    lines += [f"- {item}" for item in result["gate_adjustments"]] or ["- None"]
    lines += ["", "> EAIMS is decision support, not certification, compliance, safety, or legal assurance.", ""]
    return "\n".join(lines)


def html_report(result: dict[str, Any]) -> str:
    rows = "".join(f"<tr><td>{escape(k)}</td><td>{v:.2f}</td></tr>" for k, v in result["dimension_scores"].items())
    gates = "".join(f"<li>{escape(x)}</li>" for x in result["gate_adjustments"]) or "<li>None</li>"
    return f"""<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width\"><title>EAIMS report</title><style>body{{font:16px system-ui;max-width:900px;margin:40px auto;padding:0 20px;color:#172033}}table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;border-bottom:1px solid #d9dfeb;text-align:left}}.score{{font-size:3rem;font-weight:750;color:#155eef}}.note{{background:#f2f5fa;padding:16px;border-radius:10px}}</style><h1>EAIMS Assessment</h1><h2>{escape(result['organization'])}</h2><div class=\"score\">Level {result['final_level']}</div><p>Aggregate: {result['aggregate_score']:.2f} · Version {escape(result['version'])}</p><table><thead><tr><th>Dimension</th><th>Score</th></tr></thead><tbody>{rows}</tbody></table><h2>Gate adjustments</h2><ul>{gates}</ul><p class=\"note\">EAIMS is decision support, not certification, compliance, safety, or legal assurance.</p></html>"""
