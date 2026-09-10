from __future__ import annotations
from .engine import now_iso


def _fmt_index(value):
    return "—" if value is None else f"{value:.2f}"


def render_markdown(result: dict) -> str:
    gates = [g for g in result["gate_results"] if g["result"] in {"BREACH", "INCOMPLETE"}]
    assessment_type = result["assessment_type"]
    if assessment_type == "FULL":
        if result.get("enterprise_maturity_established"):
            scope_line = f"- Enterprise index: **{_fmt_index(result.get('enterprise_index'))}** ({result.get('enterprise_band')})"
        else:
            scope_line = "- Enterprise maturity: **NOT ESTABLISHED** (coverage requirements not met)"
    elif assessment_type == "PARTIAL":
        scope_line = f"- Indicative scoped index: **{_fmt_index(result.get('indicative_scoped_index'))}**"
    else:
        scope_line = "- Targeted assessment: **profile only; no enterprise-wide index produced**"

    lines = [
        f"# EAIMS Assessment Report — {result['assessment_id']}", "",
        f"- Specification: `{result['spec_version']}`",
        f"- Report generated at: `{now_iso()}`",
        f"- Evidence cutoff: `{result['evidence_cutoff_time']}`",
        f"- Assessment type: `{assessment_type}`",
        f"- System: **{result['system'].get('name', 'Unnamed')}**",
        f"- Derived risk band: **{result['risk_profile']['derived_band']}**",
        scope_line,
        f"- Autonomy debt: **{result.get('autonomy_debt', {}).get('level', '—')}**",
        f"- Result hash: `{result['result_hash']}`", "",
        "## Coverage", "",
        f"- Capabilities in scope: **{result.get('coverage', {}).get('capabilities_in_scope', 0)}**",
        f"- Applicable determinate ratio: **{result.get('coverage', {}).get('applicable_determinate_ratio', 0):.0%}**",
        f"- Critical capabilities assessed: **{result.get('coverage', {}).get('critical_capabilities_assessed', False)}**",
        f"- Dimensions represented: **{result.get('coverage', {}).get('dimensions_represented', 0)}/8**", "",
        "## Dimension profile", "", "| Dimension | Index |", "|---|---:|",
    ]
    for d, v in result.get("dimension_profile", {}).items():
        lines.append(f"| {d} | {_fmt_index(v)} |")
    lines += ["", "## Capability results", "", "| Capability | Result | Confidence |", "|---|---:|---:|"]
    for c in result["capability_results"]:
        lines.append(f"| {c['capability_id']} | {c['result']} | {c.get('confidence', '—')} |")
    lines += ["", "## Gate findings", ""]
    if not gates:
        lines.append("No gate breaches or incomplete active gates.")
    else:
        for g in gates:
            lines.append(f"- **{g['gate_id']} {g['result']}** — {g['title']}: {g['reason']}")
    lines += ["", "## Agent Permission Envelope", ""]
    pe = result.get("permission_envelope_evaluation", {})
    if not pe.get("applicable"):
        lines.append("Not applicable.")
    elif not pe.get("violations"):
        lines.append("No machine-detectable permission-envelope violations observed.")
    else:
        for v in pe.get("violations", []):
            lines.append(f"- **{v.get('severity', 'MATERIAL')}** — {v['type']}" + (f" (`{v.get('event_id')}`)" if v.get('event_id') else ""))
    lines += ["", "## Human Accountability Boundary", ""]
    hab = result.get("hab_evaluation", {})
    if not hab.get("applicable"):
        lines.append("Not applicable to this reference context.")
    else:
        lines.append(f"- Final authority: **{hab.get('final_authority') or 'UNDEFINED'}**")
        lines.append(f"- Human Reserved decisions: **{len(hab.get('human_reserved_decisions', []))}**")
        lines.append(f"- Recourse available: **{hab.get('recourse_available')}**")
        lines.append(f"- Intervention feasible: **{hab.get('intervention_feasible')}**")
        if hab.get("violations"):
            for v in hab["violations"]:
                lines.append(f"- **{v.get('severity', 'MATERIAL')}** — {v['type']}" + (f" (`{v.get('event_id')}`)" if v.get('event_id') else ""))
        else:
            lines.append("- No machine-detectable HAB execution violations observed.")
    lines += ["", "## Consistency findings", ""]
    if not result["consistency_findings"]:
        lines.append("No modeled consistency contradictions detected.")
    else:
        for f in result["consistency_findings"]:
            lines.append(f"- **{f['severity']} {f['rule_id']}** — {f['message']}")
    lines += ["", "## Validation note", "",
              "This result demonstrates deterministic execution of selected EAIMS rules. Synthetic reference implementations do not constitute empirical validation, certification, regulatory conformity, or production deployment assurance."]
    return "\n".join(lines) + "\n"
