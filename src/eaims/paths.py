from __future__ import annotations
from pathlib import Path
import os, sys


def resolve_data_root() -> Path:
    """Locate the EAIMS structured specification root.

    Search order:
    1. explicit EAIMS_ROOT environment variable;
    2. source/repository checkout root;
    3. current working directory;
    4. installed wheel data directory under sys.prefix/share/eaims.

    A root is valid only when it contains spec/core.yaml.
    """
    candidates=[]
    if os.environ.get("EAIMS_ROOT"):
        candidates.append(Path(os.environ["EAIMS_ROOT"]).expanduser().resolve())
    module_path = Path(__file__).resolve()
    candidates.extend([
        module_path.parents[2],
        module_path.parents[1] / "share" / "eaims",  # pip --target / local prefix installs
        Path.cwd().resolve(),
        Path(sys.prefix).resolve()/"share"/"eaims",
    ])
    seen=set()
    for root in candidates:
        key=str(root)
        if key in seen:
            continue
        seen.add(key)
        if (root/"spec"/"core.yaml").exists():
            return root
    searched=", ".join(str(x) for x in candidates)
    raise RuntimeError(
        "EAIMS specification data could not be located. "
        "Set EAIMS_ROOT to a directory containing spec/core.yaml. "
        f"Searched: {searched}"
    )

ROOT = resolve_data_root()
