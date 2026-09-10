from pathlib import Path
import importlib, os


def test_source_checkout_root_contains_canonical_spec():
    from src.eaims.paths import ROOT
    assert (ROOT / "spec" / "core.yaml").exists()


def test_explicit_eaims_root_resolution(tmp_path, monkeypatch):
    root=tmp_path/"candidate"
    (root/"spec").mkdir(parents=True)
    (root/"spec"/"core.yaml").write_text("spec_version: test\n",encoding="utf-8")
    monkeypatch.setenv("EAIMS_ROOT",str(root))
    import src.eaims.paths as paths
    assert paths.resolve_data_root()==root.resolve()
