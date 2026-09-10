from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTS = {'.md', '.yaml', '.yml', '.json', '.toml', '.py', '.txt'}
ALLOWED_PERSON = 'Elias Naserkhaki'


def iter_text():
    for p in ROOT.rglob('*'):
        if p.is_file() and p.suffix.lower() in TEXT_EXTS and '.git' not in p.parts:
            try:
                yield p, p.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                pass


def test_project_author_metadata_names_only_owner():
    pyproject = (ROOT / 'pyproject.toml').read_text(encoding='utf-8')
    assert f'name = "{ALLOWED_PERSON}"' in pyproject
    author_block = re.search(r'authors\s*=\s*\[(.*?)\]', pyproject, re.S)
    assert author_block
    assert author_block.group(1).count('name =') == 1


def test_public_attribution_files_name_only_owner():
    policy = (ROOT / 'ATTRIBUTION-POLICY.md').read_text(encoding='utf-8')
    assert ALLOWED_PERSON in policy
    # Review and assessor artifacts must use non-personal identifiers only.
    for rel in (
        'review/FEEDBACK-TEMPLATE.yaml',
        'review/RESOLUTION-TEMPLATE.yaml',
        'validation/assessor-record-example.yaml',
        'validation/review-workflow-fixture.yaml',
    ):
        text = (ROOT / rel).read_text(encoding='utf-8')
        assert 'reviewer_name' not in text
        assert 'assessor_name' not in text


def test_review_template_uses_non_personal_reviewer_id():
    tpl = (ROOT / 'review/FEEDBACK-TEMPLATE.yaml').read_text(encoding='utf-8')
    assert 'reviewer_id:' in tpl
    assert 'reviewer_name' not in tpl
