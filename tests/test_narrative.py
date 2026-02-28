"""
Tests for Narrative System
"""
import pytest

from business_radar_core.utils.narrative import (
    get_narrative_explanation,
    get_short_answer_warning,
    BASE_NARRATIVE,
    SPECIAL_NARRATIVES,
)


class TestNarrativeSystem:
    """Test narrative system functionality"""

    def test_base_narrative_kz(self):
        """Test base narrative in Kazakh"""
        text = get_narrative_explanation(None, "unknown", "kk", False)
        assert "Қазір маңызды сұрақ" in text

    def test_base_narrative_ru(self):
        """Test base narrative in Russian"""
        text = get_narrative_explanation(None, "unknown", "ru", False)
        assert "Сейчас важный вопрос" in text

    def test_first_question_narrative_kz(self):
        """Test first question narrative in Kazakh"""
        text = get_narrative_explanation(None, "unknown", "kk", True)
        assert "Бұл тест емес" in text

    def test_first_question_narrative_ru(self):
        """Test first question narrative in Russian"""
        text = get_narrative_explanation(None, "unknown", "ru", True)
        assert "Это не тест" in text

    def test_special_narrative_amount(self):
        """Test special narrative for amount"""
        assert "amount" in SPECIAL_NARRATIVES
        assert "kk" in SPECIAL_NARRATIVES["amount"]
        assert "ru" in SPECIAL_NARRATIVES["amount"]

    def test_special_narrative_idea(self):
        """Test special narrative for idea"""
        assert "idea_description" in SPECIAL_NARRATIVES

    def test_short_answer_warning_kz(self):
        """Test short answer warning in Kazakh"""
        text = get_short_answer_warning("kk")
        assert "қателесуім мүмкін" in text

    def test_short_answer_warning_ru(self):
        """Test short answer warning in Russian"""
        text = get_short_answer_warning("ru")
        assert "могу ошибиться" in text

    def test_base_narrative_structure(self):
        """Test base narrative structure"""
        assert "kk" in BASE_NARRATIVE
        assert "ru" in BASE_NARRATIVE
        assert "explanation" in BASE_NARRATIVE["kk"]
        assert "warning" in BASE_NARRATIVE["kk"]
