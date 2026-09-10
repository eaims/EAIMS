from __future__ import annotations
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
errors=[]
warnings=[]
required = [
    'LICENSE','LICENSE-CODE.md','LICENSE-DOCS.md','LICENSES/Apache-2.0.txt','LICENSES/CC-BY-4.0.txt',
    'CONTRIBUTING.md','IP_POLICY.md','GOVERNANCE.md','AUTHORS.md','CONTRIBUTORS.md',
    'ATTRIBUTION-POLICY.md','CONTRIBUTOR-RIGHTS.md','TRADEMARK.md','CLA.md',
    'COPYRIGHT-ASSIGNMENT.md','DISCLAIMER.md','ORIGIN.md','THIRD_PARTY_NOTICES.md','PROVENANCE.md','DCO.md'
]
for rel in required:
    if not (ROOT/rel).is_file(): errors.append(f'missing required legal/provenance file: {rel}')

def text(rel): return (ROOT/rel).read_text(encoding='utf-8')

def require(rel, *phrases):
    t=text(rel)
    for phrase in phrases:
        if phrase not in t: errors.append(f'{rel}: missing required concept/phrase: {phrase}')

# Ownership/public-license boundary and non-retroactivity.
require('LICENSE',
        'Copyright © 2026 Elias Naserkhaki. All rights reserved except as expressly licensed.',
        'not retroactively revoked', 'CC BY 4.0', 'Apache-2.0',
        'Substantive Contribution', 'CLA may provide broad project rights')
require('LICENSE-CODE.md','tests','Docker/Compose','JSON Schemas','Apache License 2.0')
require('LICENSE-DOCS.md','machine-readable specification data','JSON Schema files','CC BY 4.0')

# Mandatory substantive contribution gate.
for rel in ['IP_POLICY.md','CONTRIBUTOR-RIGHTS.md','CONTRIBUTING.md']:
    t=text(rel)
    if not (re.search(r'Substantive Contribution', t, re.I) and re.search(r'(MUST NOT|SHALL NOT|MUST complete|SHALL be incorporated.*until)', t, re.I|re.S) and re.search(r'incorporat', t, re.I)):
        errors.append(f'{rel}: mandatory substantive-contribution incorporation gate not found')
if 'does not replace' not in text('CONTRIBUTING.md') or 'DCO' not in text('CONTRIBUTING.md'):
    errors.append('CONTRIBUTING.md: DCO/CLA distinction missing')

# CLA rights breadth, patent permission, no joint work.
for term in ['perpetual','worldwide','irrevocable','transferable','sublicensable','relicense','dual-license','proprietary','patent license','joint authorship']:
    if term.lower() not in text('CLA.md').lower(): errors.append(f'CLA.md: missing {term}')
# Assignment breadth, patent permission, fallback, no joint work.
for term in ['assigns, transfers, and conveys','sublicense','relicense','dual-license','proprietarily relicense','fallback license','patent license','joint authorship']:
    if term.lower() not in text('COPYRIGHT-ASSIGNMENT.md').lower(): errors.append(f'COPYRIGHT-ASSIGNMENT.md: missing {term}')

# Governance reserved authority.
for term in ['editorial acceptance','release approval','dual-licensing','sublicensing','relicensing','commercial licensing','proprietary relicensing','future versions','final governance decisions']:
    if term.lower() not in text('GOVERNANCE.md').lower(): errors.append(f'GOVERNANCE.md: missing reserved authority: {term}')

# No implied co-authorship/co-ownership/governance.
for rel in ['AUTHORS.md','CONTRIBUTORS.md','ATTRIBUTION-POLICY.md','CONTRIBUTOR-RIGHTS.md','GOVERNANCE.md','CLA.md','COPYRIGHT-ASSIGNMENT.md']:
    tl=text(rel).lower()
    for concept in ['co-authorship','governance']:
        if concept not in tl: errors.append(f'{rel}: missing no-implied-{concept} coverage')

# Attribution carve-outs and named-role policy.
require('ATTRIBUTION-POLICY.md','legally required attribution','bibliographic citation','external review records','third-party material','external assessor','feasibility-probe author','contributor of findings')

# Trademark separation.
require('TRADEMARK.md','separate from copyright','do not grant trademark rights','official EAIMS','Reservation of rights')

# Third-party/provenance records and no direct-incorporation loophole.
require('THIRD_PARTY_NOTICES.md','not vendored','rights-instrument requirements','did not identify any known directly incorporated substantive third-party text, code, or artifact')
require('PROVENANCE.md','Original EAIMS material','Third-party software dependencies','External findings, reviews, and design inputs','Trademarks and project identity','Governance authority')

# Package metadata / license notice alignment.
py=text('pyproject.toml')
if 'name = "Elias Naserkhaki"' not in py: errors.append('pyproject: project author not Elias Naserkhaki')
for token in ['LICENSE-CODE.md','LICENSE-DOCS.md','THIRD_PARTY_NOTICES.md','ATTRIBUTION-POLICY.md']:
    if token not in py: errors.append(f'pyproject: packaged legal notice missing: {token}')
for term in ['tests','Docker/Compose','JSON Schemas','CC BY 4.0','Apache-2.0']:
    if term not in text('PACKAGE-LICENSE-NOTICE.md'): errors.append(f'PACKAGE-LICENSE-NOTICE.md: missing boundary term: {term}')

# No other person presented in authorship metadata or public role files.
if text('AUTHORS.md').count('**Elias Naserkhaki**') != 1:
    errors.append('AUTHORS.md: expected exactly one named founder/authorship entry')
cff=text('CITATION.cff')
if cff.count('family-names:') != 1: errors.append('CITATION.cff: expected exactly one author')
if 'family-names: Naserkhaki' not in cff or 'given-names: Elias' not in cff: errors.append('CITATION.cff: unexpected author identity')

# Detect public identity leakage in structured review/assessor records.
for rel in ['review/FEEDBACK-TEMPLATE.yaml','review/RESOLUTION-TEMPLATE.yaml','validation/assessor-record-example.yaml','validation/review-workflow-fixture.yaml']:
    t=text(rel)
    if re.search(r'\b(?:reviewer|assessor)_name(?:_or_pseudonym)?\b',t,re.I): errors.append(f'{rel}: personal-name field present')

# Detect realistic email leakage; allow only project-controlled address if ever intentionally present.
email_re=re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
for p in ROOT.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in {'.md','.yaml','.yml','.json','.toml','.py','.txt','.cff'}: continue
    rel=p.relative_to(ROOT)
    if any(part in {'.pytest_cache','__pycache__','dist','build'} for part in rel.parts): continue
    t=p.read_text(encoding='utf-8',errors='ignore')
    for e in email_re.findall(t):
        if True:
            errors.append(f'{rel}: unexpected email address: {e}')

# Obsolete legal-integration statements must not remain active.
obsolete=['Legal/governance files are deliberately not duplicated into FC16','Existing repository legal/governance assets identified for preservation.']
for p in ROOT.rglob('*.md'):
    t=p.read_text(encoding='utf-8',errors='ignore')
    for phrase in obsolete:
        if phrase in t: errors.append(f'{p.relative_to(ROOT)}: obsolete legal integration statement remains')

# Full license copies sanity checks (matching standard packaged byte sizes used by prior EAIMS repo).
expected_sizes={'LICENSES/Apache-2.0.txt':11358,'LICENSES/CC-BY-4.0.txt':18657}
for rel,size in expected_sizes.items():
    if (ROOT/rel).exists() and (ROOT/rel).stat().st_size != size:
        warnings.append(f'{rel}: license text size differs from expected baseline ({(ROOT/rel).stat().st_size} vs {size}); verify exact text')

status='PASS' if not errors else 'FAIL'
result={'status':status,'errors':errors,'warnings':warnings,'required_files_checked':len(required),'github_push_merge_release_performed_by_this_audit':False}
print(json.dumps(result,indent=2,ensure_ascii=False))
(ROOT/'validation/legal-ip-governance-audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
raise SystemExit(0 if not errors else 1)
