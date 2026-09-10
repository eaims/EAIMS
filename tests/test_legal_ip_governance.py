from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]

def read(p): return (ROOT/p).read_text(encoding='utf-8')

def test_mandatory_substantive_contribution_rights_gate():
    assert 'No Substantive Contribution from a third party SHALL be incorporated' in read('IP_POLICY.md')
    assert 'MUST NOT be incorporated into an official EAIMS release' in read('CONTRIBUTOR-RIGHTS.md')
    assert 'MUST complete a project-approved CLA or copyright assignment' in read('CONTRIBUTING.md')

def test_governance_reserved_authority_and_license_continuity():
    g=read('GOVERNANCE.md')
    for term in ['editorial acceptance','release approval','dual-licensing','sublicensing','relicensing','proprietary relicensing','final governance decisions']:
        assert term in g
    assert 'not retroactively revoked' in g

def test_cla_and_assignment_preserve_relicensing_control_without_false_coownership():
    cla=read('CLA.md').lower(); ass=read('COPYRIGHT-ASSIGNMENT.md').lower()
    for t in ['sublicensable','relicense','dual-license','proprietary','patent license','joint authorship']:
        assert t in cla
    for t in ['assigns, transfers, and conveys','relicense','dual-license','proprietarily relicense','patent license','joint authorship']:
        assert t in ass

def test_license_boundary_is_explicit():
    lic=read('LICENSE')
    assert 'machine-readable specification/assessment data in YAML or JSON' in lic
    assert 'except JSON Schema files' in lic
    assert 'tests, automation and build scripts' in lic
    assert 'Docker/Compose configuration' in lic

def test_public_authorship_metadata_has_only_elias():
    assert read('CITATION.cff').count('family-names:') == 1
    assert 'family-names: Naserkhaki' in read('CITATION.cff')
    assert read('AUTHORS.md').count('**Elias Naserkhaki**') == 1
