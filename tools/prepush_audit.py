from pathlib import Path
import json, re, yaml, sys
from yaml.constructor import ConstructorError

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
errors=[]
warnings=[]
EXPECTED_SPEC='1.0.0-fc16'
EXPECTED_RELEASE=(ROOT/'VERSION').read_text(encoding='utf-8').strip()
EXPECTED_PACKAGE=EXPECTED_RELEASE

class DupCheckLoader(yaml.SafeLoader):
    pass

def _construct_mapping(loader,node,deep=False):
    mapping={}
    for key_node,value_node in node.value:
        key=loader.construct_object(key_node,deep=deep)
        if key in mapping:
            raise ConstructorError('while constructing a mapping',node.start_mark,f'duplicate key: {key}',key_node.start_mark)
        mapping[key]=loader.construct_object(value_node,deep=deep)
    return mapping
DupCheckLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,_construct_mapping)

def _json_no_dups(text):
    def hook(pairs):
        out={}
        for k,v in pairs:
            if k in out: raise ValueError(f'duplicate key: {k}')
            out[k]=v
        return out
    return json.loads(text,object_pairs_hook=hook)

core=yaml.safe_load((ROOT/'spec/core.yaml').read_text())
version=core['spec_version']
if version!=EXPECTED_SPEC: errors.append(f'unexpected spec provenance version: {version}')
pyproject=(ROOT/'pyproject.toml').read_text()
if f'version = "{EXPECTED_PACKAGE}"' not in pyproject: errors.append('unexpected package version')
if 'name = "eaims"' not in pyproject: errors.append('package identity is not eaims')
if 'name = "Elias Naserkhaki"' not in pyproject: errors.append('project author metadata is not Elias Naserkhaki')

package_init=(ROOT/'src/eaims/__init__.py').read_text(encoding='utf-8')
if f'__version__ = "{EXPECTED_PACKAGE}"' not in package_init:
    errors.append('runtime package version mismatch')
for rel in ('docker-compose.yml', 'docker-compose.reference.yml'):
    compose=yaml.safe_load((ROOT/rel).read_text(encoding='utf-8'))
    for service in compose.get('services', {}).values():
        image=service.get('image', '')
        if image.startswith('eaims/validator:') and image != f'eaims/validator:{EXPECTED_PACKAGE}':
            errors.append(f'{rel}: validator image version mismatch')

version_file=(ROOT/'VERSION').read_text(encoding='utf-8').strip()
if version_file!=EXPECTED_RELEASE: errors.append(f'unexpected VERSION file: {version_file}')
citation=(ROOT/'CITATION.cff').read_text(encoding='utf-8')
if f'version: "{EXPECTED_RELEASE}"' not in citation: errors.append('CITATION.cff release version mismatch')
citation_data=yaml.safe_load(citation)
release_date=str(citation_data.get('date-released',''))
if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', release_date):
    errors.append('CITATION.cff release date missing or invalid')

# Active-stage files must not carry stale pre-FC16 candidate tags.
for rel in ['README.md','VALIDATION.md','pyproject.toml','docker-compose.yml','docker-compose.reference.yml','research/EVOLUTION-0.2x-to-1.0.md']:
    text=(ROOT/rel).read_text()
    stale=sorted(set(re.findall(r'\b(?:FC|fc)(?:[0-9]|1[0-5])\b|\bdev1[0-5]\b', text)))
    if stale: errors.append(f'{rel}: stale labels {stale}')

# Public release-facing metadata must no longer identify the release itself as a candidate.
for rel in ['README.md','VALIDATION.md','VERSION','CITATION.cff','pyproject.toml','docker-compose.yml','docker-compose.reference.yml']:
    text=(ROOT/rel).read_text(encoding='utf-8')
    if '1.0.0-rc.1-candidate' in text or '1.0.0.dev16' in text:
        errors.append(f'{rel}: stale RC/development release metadata')

# Structured files must parse and must not contain duplicate mapping keys.
for p in ROOT.rglob('*'):
    if not p.is_file(): continue
    rel=p.relative_to(ROOT)
    if any(part in {'.pytest_cache','__pycache__','dist','build'} for part in rel.parts): continue
    try:
        if p.suffix in {'.yaml','.yml'}:
            yaml.load(p.read_text(encoding='utf-8'),Loader=DupCheckLoader)
        elif p.suffix=='.json':
            _json_no_dups(p.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'parse/duplicate-key failure {rel}: {exc}')

# No local machine paths, private-key material, secret files, personal-email leakage,
# or named reviewer/assessor fields in public review artifacts.
email_re=re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
for p in ROOT.rglob('*'):
    if not p.is_file(): continue
    rel=p.relative_to(ROOT)
    if any(part in {'.pytest_cache','__pycache__','dist','build'} for part in rel.parts): continue
    if p.name in {'.env','id_rsa','id_ed25519'}: errors.append(f'sensitive file present: {rel}')
    if rel in {Path('tools/prepush_audit.py'), Path('tools/legal_ip_governance_audit.py')}: continue
    if p.suffix.lower() in {'.md','.py','.yaml','.yml','.json','.toml','.txt'}:
        text=p.read_text(encoding='utf-8',errors='ignore')
        if '/mnt/data/' in text or '/home/oai/' in text: errors.append(f'local build path leaked: {rel}')
        if '-----BEGIN PRIVATE KEY-----' in text: errors.append(f'private key material detected: {rel}')
        if email_re.search(text): errors.append(f'email address present in public candidate: {rel}')
        if rel.parts and rel.parts[0] in {'review','validation'}:
            if re.search(r'\b(?:reviewer|assessor)_name(?:_or_pseudonym)?\b',text,re.I):
                errors.append(f'personal-name field present in review/assessor artifact: {rel}')

# Canonical semantic integrity must pass the same validator used by CI.
try:
    from src.eaims.validate import validate_referential_integrity
    errors.extend(f'spec integrity: {e}' for e in validate_referential_integrity())
except Exception as exc:
    errors.append(f'could not execute canonical validator: {exc}')

# Readiness assertions must remain conservative.
r=json.loads((ROOT/'validation/rc-review-readiness.json').read_text())
if r.get('independent_review_completed') is True: errors.append('independent review incorrectly marked complete')
m=json.loads((ROOT/'manifest.json').read_text()) if (ROOT/'manifest.json').exists() else {}
if m.get('github_push_performed') is True: errors.append('manifest incorrectly states GitHub push performed')

# Packaging contract alignment.
if 'share/eaims/spec' not in pyproject: errors.append('installed-package spec data mapping missing')
if not (ROOT/'src/eaims/paths.py').exists(): errors.append('installed-package data-root resolver missing')
for command in ('"assess"','"validate-fixture"','"validate"','"score"','"report"','"review"'):
    if command not in (ROOT/'src/eaims/cli.py').read_text(): warnings.append(f'CLI command token not found: {command}')

print(json.dumps({'spec_version':version,'package_version':EXPECTED_PACKAGE,'release_version':EXPECTED_RELEASE,'errors':errors,'warnings':warnings,'status':'PASS' if not errors else 'FAIL'},indent=2))
raise SystemExit(1 if errors else 0)
