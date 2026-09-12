from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "spec" / "adversarial-agentic-1.1-draft.yaml"
MV = ROOT / "spec" / "adversarial-agentic-machine-verification-1.1-draft.yaml"


def _load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_v11_machine_rules_cover_only_mv2_candidate_requirements():
    profile = _load(PROFILE)
    mv = _load(MV)
    candidates = {r["requirement_id"]: r for r in profile["candidate_requirements"]}
    covered = {r["requirement_id"] for r in mv["rules"]}

    assert covered == {
        rid for rid, req in candidates.items()
        if req["machine_verifiability"] == "MV2"
    }


def test_v11_machine_rules_use_unique_paths_and_supported_operators():
    mv = _load(MV)
    paths = [r["path"] for r in mv["rules"]]
    operators = {r["operator"] for r in mv["rules"]}

    assert len(paths) == len(set(paths))
    assert operators.issubset({"truthy", "nonempty", "all_nonempty", "enum"})


def test_v11_machine_rules_do_not_reuse_v1_paths():
    base = _load(ROOT / "spec" / "machine-verification.yaml")
    mv = _load(MV)
    base_paths = {r["path"] for r in base["rules"]}
    draft_paths = {r["path"] for r in mv["rules"]}
    assert base_paths.isdisjoint(draft_paths)
