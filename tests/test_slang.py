"""
Tests for Slang Normalizer
"""
import pytest

from business_radar_core.utils.slang import SlangNormalizer


class TestSlangNormalizer:
    """Test slang normalization functionality"""

    def setup_method(self):
        """Setup test fixtures"""
        self.normalizer = SlangNormalizer()

    def test_normalize_lam(self):
        """Test normalization: лям → миллион"""
        result = self.normalizer.normalize("лям теңге")
        assert "миллион" in result

    def test_normalize_tenge(self):
        """Test normalization: теңге → тенге"""
        result = self.normalizer.normalize("500 теңге")
        assert "тенге" in result

    def test_normalize_filler_removal(self):
        """Test removal of filler words"""
        result = self.normalizer.normalize("короче, ну, долг 500 тысяч")
        assert "короче" not in result
        assert "ну" not in result

    def test_extract_amounts(self):
        """Test amount entity extraction"""
        entities = self.normalizer.extract_entities("Долг 500 тысяч тенге")
        assert "amounts" in entities

    def test_extract_cities(self):
        """Test city entity extraction"""
        entities = self.normalizer.extract_entities("Алматыда, 500 мың")
        assert "cities" in entities
        assert any("Алматы" in str(e) for e in entities["cities"])

    def test_normalize_mixed_speech(self):
        """Test normalization of mixed Kazakh-Russian speech"""
        result = self.normalizer.normalize("Короче, лям теңге қарыз, Алматыда")
        assert "миллион" in result
        assert "тенге" in result
        assert "Алматы" in result

    def test_add_custom_slang(self):
        """Test adding custom slang"""
        self.normalizer.add_custom_slang("тестовое", "тест")
        result = self.normalizer.normalize("тестовое слово")
        assert "тест" in result
