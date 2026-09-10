"""Structural validation of the v1 fixture before semantic evaluation."""
from __future__ import annotations

import json
import math
from typing import Any
from jsonschema import Draft202012Validator, FormatChecker
from .paths import ROOT


def validate_input_structure(value: Any) -> list[str]:
    errors = []
    active = set()

    def walk(node: Any, path: str) -> None:
        if isinstance(node, float) and not math.isfinite(node):
            errors.append(f"{path}: number must be finite")
        elif isinstance(node, (dict, list)):
            if id(node) in active:
                errors.append(f"{path}: recursive data is not supported")
                return
            active.add(id(node))
            entries = node.items() if isinstance(node, dict) else enumerate(node)
            for key, child in entries:
                if isinstance(node, dict) and not isinstance(key, str):
                    errors.append(f"{path}: object keys must be strings")
                walk(child, f"{path}.{key}")
            active.remove(id(node))
        elif node is not None and not isinstance(node, (str, int, float, bool)):
            errors.append(f"{path}: value must be JSON-compatible")

    walk(value, "$")
    if errors:
        return errors
    schema = json.loads((ROOT / "schemas" / "assessment-fixture-v1.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(value), key=lambda e: tuple(map(str, e.path))):
        path = ".".join(map(str, error.path)) or "$"
        errors.append(f"{path}: {error.message}")
    return errors
