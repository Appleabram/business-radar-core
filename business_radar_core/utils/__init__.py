"""
Utility modules for Business Radar Bot
"""

from business_radar_core.utils.narrative import (
    get_narrative_explanation,
    get_question,
    get_short_answer_warning,
    get_voice_confirmation,
    BASE_NARRATIVE,
    SPECIAL_NARRATIVES,
)
from business_radar_core.utils.slang import SlangNormalizer, normalizer

__all__ = [
    "get_narrative_explanation",
    "get_question",
    "get_short_answer_warning",
    "get_voice_confirmation",
    "BASE_NARRATIVE",
    "SPECIAL_NARRATIVES",
    "SlangNormalizer",
    "normalizer",
]
