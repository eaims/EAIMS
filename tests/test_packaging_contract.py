from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]

def test_pyproject_exposes_cli():
    text=(ROOT/'pyproject.toml').read_text()
    assert 'eaims = "eaims.cli:main"' in text
    assert 'eaims-validate = "eaims.validate:main"' in text

def test_dockerfile_non_root_and_pinned_python_line():
    text=(ROOT/'Dockerfile.validator').read_text()
    assert text.startswith('FROM python:3.12-slim')
    assert 'USER eaims' in text
    assert 'ENTRYPOINT ["eaims-validate"]' in text

def test_minimal_compose_security_contract():
    d=yaml.safe_load((ROOT/'docker-compose.yml').read_text())
    v=d['services']['validator']
    assert v['read_only'] is True
    assert 'no-new-privileges:true' in v['security_opt']
    assert 'ALL' in v['cap_drop']

def test_reference_compose_has_only_wired_reference_services():
    d=yaml.safe_load((ROOT/'docker-compose.reference.yml').read_text())
    assert {'validator','reference-runner'} <= set(d['services'])
    assert 'evidence-store' not in d['services']

def test_packaging_contract_declares_no_runtime_claim():
    d=yaml.safe_load((ROOT/'validation/packaging-contract.yaml').read_text())
    assert d['runtime_contract']['runtime_claim_status'].startswith('not_container-runtime-validated')
