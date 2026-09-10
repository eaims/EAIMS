from __future__ import annotations
from pathlib import Path
from .paths import ROOT
from typing import Any
import yaml



def _get_path(obj: dict[str, Any], path: str):
    cur: Any=obj
    for part in path.split('.'):
        if not isinstance(cur,dict) or part not in cur:
            return None
        cur=cur[part]
    return cur


def evaluate_rule(rule: dict[str,Any], context: dict[str,Any]) -> dict[str,Any]:
    value=_get_path(context,rule['path'])
    op=rule['operator']
    passed=False
    if op=='truthy': passed = value is True
    elif op=='nonempty': passed = value is not None and hasattr(value,'__len__') and len(value)>0
    elif op=='enum': passed = value in set(rule.get('allowed_values',[]))
    elif op=='all_nonempty':
        passed = isinstance(value,dict) and all(value.get(k) not in (None,'',[]) for k in rule.get('required_keys',[]))
    else: raise ValueError(f"unsupported operator: {op}")
    return {
        'requirement_id':rule['requirement_id'],
        'result':'SATISFIED' if passed else 'NOT_SATISFIED',
        'operator':op,
        'path':rule['path'],
        'observed':value,
    }


def verify_critical_machine_requirements(context: dict[str,Any], spec_path: Path|None=None) -> list[dict[str,Any]]:
    spec_path=spec_path or ROOT/'spec'/'machine-verification.yaml'
    spec=yaml.safe_load(spec_path.read_text(encoding='utf-8'))
    return [evaluate_rule(r,context) for r in spec['rules']]


def mutate_to_fail(rule: dict[str,Any], context: dict[str,Any]) -> dict[str,Any]:
    import copy
    c=copy.deepcopy(context)
    parts=rule['path'].split('.')
    cur=c
    for p in parts[:-1]:
        cur=cur.setdefault(p,{})
    op=rule['operator']
    if op=='truthy': cur[parts[-1]]=False
    elif op=='nonempty': cur[parts[-1]]=[]
    elif op=='enum': cur[parts[-1]]='INVALID'
    elif op=='all_nonempty':
        v=cur.setdefault(parts[-1],{})
        v[rule['required_keys'][0]]=''
    return c
