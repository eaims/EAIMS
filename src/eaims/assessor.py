from __future__ import annotations
from pathlib import Path
from .paths import ROOT
from typing import Any
import yaml

ALLOWED={'SATISFIED','NOT_SATISFIED','INSUFFICIENT_EVIDENCE','NOT_APPLICABLE'}


def protocol_index(path: Path|None=None):
    path=path or ROOT/'spec'/'assessor-protocol.yaml'
    doc=yaml.safe_load(path.read_text(encoding='utf-8'))
    return {p['requirement_id']:p for p in doc['protocol']}


def validate_assessor_record(record: dict[str,Any], protocol: dict[str,Any]|None=None) -> list[str]:
    errors=[]
    protocol=protocol or protocol_index().get(record.get('requirement_id'))
    if not protocol:
        return ['unknown_or_unscoped_requirement']
    for k in protocol['required_record_fields']:
        if record.get(k) in (None,'',[]): errors.append(f'missing:{k}')
    if record.get('decision') not in ALLOWED: errors.append('invalid:decision')
    if record.get('decision')=='NOT_APPLICABLE' and not record.get('applicability_rationale'):
        errors.append('missing:applicability_rationale')
    return errors


def normalize_assessor_result(record: dict[str,Any]) -> dict[str,Any]:
    p=protocol_index().get(record.get('requirement_id'))
    errs=validate_assessor_record(record,p)
    return {
        'requirement_id':record.get('requirement_id'),
        'result':'ERROR' if errs else record.get('decision'),
        'errors':errs,
        'rationale':record.get('rationale'),
        'evidence_refs':record.get('evidence_refs',[]),
        'assessor_id':record.get('assessor_id'),
        'assessed_at':record.get('assessed_at'),
    }


CONF_RANK={"C0":0,"C1":1,"C2":2,"C3":3,"C4":4}
INDEPENDENCE={"SELF","INTERNAL_INDEPENDENT","EXTERNAL","MULTI_ASSESSOR"}


def _median_confidence(values: list[str]) -> str:
    nums=sorted(CONF_RANK[v] for v in values if v in CONF_RANK)
    if not nums:
        return "C0"
    n=len(nums)
    mid=nums[n//2] if n%2 else (nums[n//2-1]+nums[n//2])//2
    return f"C{mid}"


def assess_assessment_quality(factors: dict[str,Any]) -> dict[str,Any]:
    """Rule-based Assessment Quality diagnostic.

    Quality is deliberately separate from organizational maturity. The function emits the
    factor values and explicit reasons rather than an opaque numeric quality score.
    """
    scope=float(factors.get('scope_completeness',0) or 0)
    evidence=float(factors.get('evidence_coverage',0) or 0)
    critical=float(factors.get('critical_coverage',0) or 0)
    conflicts=int(factors.get('unresolved_conflicts',0) or 0)
    critical_conflicts=int(factors.get('critical_unresolved_conflicts',0) or 0)
    stale=float(factors.get('stale_or_invalid_evidence_ratio',0) or 0)
    independence=factors.get('assessor_independence','SELF')
    confs=factors.get('confidence_profile',[]) or []
    median=_median_confidence(confs)
    m=CONF_RANK[median]
    if independence not in INDEPENDENCE:
        raise ValueError('invalid assessor_independence')
    high=(scope>=.90 and evidence>=.85 and critical>=1.0 and m>=3 and
          critical_conflicts==0 and conflicts<=1 and stale<=.10 and independence!='SELF')
    moderate=(scope>=.70 and evidence>=.65 and critical>=.90 and m>=2 and
              critical_conflicts==0 and stale<=.25)
    level='HIGH' if high else ('MODERATE' if moderate else 'LIMITED')
    reasons=[]
    if scope<.90: reasons.append('scope_below_high_threshold')
    if evidence<.85: reasons.append('evidence_coverage_below_high_threshold')
    if critical<1.0: reasons.append('critical_coverage_not_complete')
    if m<3: reasons.append('median_confidence_below_C3')
    if conflicts>1: reasons.append('multiple_unresolved_conflicts')
    if critical_conflicts: reasons.append('critical_unresolved_conflict')
    if stale>.10: reasons.append('stale_or_invalid_evidence_above_high_threshold')
    if independence=='SELF': reasons.append('self_assessment_limits_high_quality')
    return {
        'level':level,
        'median_confidence':median,
        'factors':{
            'scope_completeness':scope,'evidence_coverage':evidence,'critical_coverage':critical,
            'unresolved_conflicts':conflicts,'critical_unresolved_conflicts':critical_conflicts,
            'stale_or_invalid_evidence_ratio':stale,'assessor_independence':independence,
        },
        'reasons':reasons,
        'maturity_effect':'NONE',
    }


def detect_multi_assessor_disagreements(records: list[dict[str,Any]]) -> list[dict[str,Any]]:
    """Preserve assessor judgments and classify disagreements per requirement.

    Invalid records are returned as errors rather than silently participating in consensus.
    No averaging is performed.
    """
    grouped={}
    for rec in records:
        norm=normalize_assessor_result(rec)
        grouped.setdefault(rec.get('requirement_id'),[]).append({**norm,'independence_class':rec.get('independence_class')})
    out=[]
    for rid,items in sorted(grouped.items(), key=lambda x:str(x[0])):
        valid=[i for i in items if i['result']!='ERROR']
        decisions={i['result'] for i in valid}
        if not valid:
            cls='ERROR'
        elif len(decisions)<=1:
            cls='NONE'
        elif 'NOT_APPLICABLE' in decisions:
            cls='APPLICABILITY'
        elif 'SATISFIED' in decisions and 'NOT_SATISFIED' in decisions:
            cls='MATERIAL'
        elif 'INSUFFICIENT_EVIDENCE' in decisions:
            cls='EVIDENCE'
        else:
            cls='MATERIAL'
        out.append({
            'requirement_id':rid,
            'disagreement_class':cls,
            'resolution_required':cls not in {'NONE'},
            'decisions':sorted(decisions),
            'assessor_ids':[i.get('assessor_id') for i in valid],
            'records':items,
        })
    return out


def validate_resolution_record(resolution: dict[str,Any], disagreement: dict[str,Any]|None=None) -> list[str]:
    errors=[]
    required=['requirement_id','resolver_id','final_decision','rationale','evidence_refs','considered_assessor_ids','resolved_at']
    for k in required:
        if resolution.get(k) in (None,'',[]): errors.append(f'missing:{k}')
    if resolution.get('final_decision') not in ALLOWED: errors.append('invalid:final_decision')
    if disagreement:
        if resolution.get('requirement_id')!=disagreement.get('requirement_id'):
            errors.append('mismatch:requirement_id')
        known=set(disagreement.get('assessor_ids',[]))
        considered=set(resolution.get('considered_assessor_ids',[]) or [])
        if known and not known.issubset(considered): errors.append('missing:considered_assessor_ids')
    return errors


def resolve_multi_assessor(disagreement: dict[str,Any], resolution: dict[str,Any]) -> dict[str,Any]:
    errs=validate_resolution_record(resolution,disagreement)
    return {
        'requirement_id':disagreement.get('requirement_id'),
        'status':'ERROR' if errs else 'RESOLVED',
        'errors':errs,
        'original_disagreement_class':disagreement.get('disagreement_class'),
        'original_records':disagreement.get('records',[]),
        'resolution':resolution if not errs else None,
        'final_decision':None if errs else resolution.get('final_decision'),
    }


def inter_rater_dataset(records: list[dict[str,Any]]) -> list[dict[str,Any]]:
    """Create a neutral, long-form export suitable for later inter-rater analysis.

    It intentionally does not claim or calculate reliability from synthetic worked cases.
    """
    out=[]
    for rec in records:
        norm=normalize_assessor_result(rec)
        if norm['result']=='ERROR':
            continue
        out.append({
            'requirement_id':rec.get('requirement_id'),
            'assessor_id':rec.get('assessor_id'),
            'decision':rec.get('decision'),
            'assessed_at':rec.get('assessed_at'),
            'independence_class':rec.get('independence_class','SELF'),
        })
    return sorted(out,key=lambda x:(x['requirement_id'],x['assessor_id']))
