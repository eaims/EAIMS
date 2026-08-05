"""EAIMS executable reference implementation."""

from .scoring import AssessmentError, score_assessment, validate_assessment

__all__ = ["AssessmentError", "score_assessment", "validate_assessment"]
__version__ = "0.2.0"
