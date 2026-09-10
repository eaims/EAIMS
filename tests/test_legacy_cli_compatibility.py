from pathlib import Path
import json
from src.eaims.cli import main


def _legacy_fixture():
    rows=[]
    for d in range(1,10):
        for c in range(1,4):
            rows.append({'capability_id':f'{d}.{c}','score':2,'confidence':'medium','evidence_ids':['E']})
    return {'standard':'EAIMS','version':'0.2.1','organization':'Example Org','assessment_date':'2026-09-09','assessment_type':'full','scope':'enterprise','capability_scores':rows}


def test_legacy_validate_score_report_commands_remain_available(tmp_path, capsys):
    src=tmp_path/'legacy.json'; src.write_text(json.dumps(_legacy_fixture()),encoding='utf-8')
    assert main(['validate',str(src)])==0
    assert main(['score',str(src)])==0
    out=tmp_path/'legacy.md'
    assert main(['report',str(src),'--output',str(out)])==0
    assert out.exists() and 'EAIMS Assessment' in out.read_text()
