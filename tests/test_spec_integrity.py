from src.eaims.validate import validate_referential_integrity, summary

def test_spec_integrity():
    assert validate_referential_integrity() == []

def test_canonical_counts():
    s=summary()
    assert s["capabilities"] == 30
    assert s["anchors"] == 150
    assert s["requirements"] >= 150
    assert s["critical_shall_requirements"] > 0
