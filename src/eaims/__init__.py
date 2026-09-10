"""EAIMS executable reference package."""

__version__ = "1.0.0.dev16"
SPEC_VERSION = "1.0.0-fc16"

# Backward-compatible public API retained from v0.2.1.
from .scoring import AssessmentError, score_assessment, validate_assessment
from .reporting import html_report, markdown_report

__all__ = [
    "AssessmentError",
    "validate_assessment",
    "score_assessment",
    "markdown_report",
    "html_report",
    "SPEC_VERSION",
]
