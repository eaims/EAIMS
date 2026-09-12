from pathlib import Path
import ast
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_public_release_versions_agree():
    version = (ROOT / 'VERSION').read_text().strip()
    pyproject = (ROOT / 'pyproject.toml').read_text()
    assert re.search(r'^version = "' + re.escape(version) + '"$', pyproject, re.M)
    tree = ast.parse((ROOT / 'src/eaims/__init__.py').read_text())
    runtime = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body
               if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
    assert runtime['__version__'] == version
    assert runtime['SPEC_VERSION'] == '1.0.0-fc16'
    assert yaml.safe_load((ROOT / 'CITATION.cff').read_text())['version'] == version
    for name in ('docker-compose.yml', 'docker-compose.reference.yml'):
        data = yaml.safe_load((ROOT / name).read_text())
        for service in data['services'].values():
            assert service['image'] == f'eaims/validator:{version}'
    assert (ROOT / f'RELEASE-NOTES-v{version}.md').is_file()


def test_release_facing_documents_match_public_version():
    version = (ROOT / 'VERSION').read_text().strip()
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    validation = (ROOT / 'VALIDATION.md').read_text(encoding='utf-8')
    assert f'**Version:** {version}' in readme
    assert f'The current public release version is **{version}**' in readme
    assert f'eaims/validator:{version}' in readme
    assert validation.startswith(f'# EAIMS {version} — Validation Status')
    assert f'The public release version is **{version}**' in validation
