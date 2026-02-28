"""
Module 5: Idea Validation (Идея тірі ме? / Идея живая или мусор)
Business logic only - no Telegram dependencies
"""
from typing import Dict, List


class IdeaVerdictGenerator:
    """
    Генератор вердиктов для модуля бизнес-идей
    
    Анализирует бизнес-идею и определяет зону:
    - 🟢 Зелёная: идея проработана
    - 🟡 Жёлтая: идея имеет право на жизнь
    - 🔴 Красная: идея сырая
    """
    
    def __init__(self):
        self.weak_points: List[str] = []
    
    def analyze(self, data: Dict) -> Dict:
        """
        Анализ бизнес-идеи
        
        :param data: Словарь с данными:
            - idea_description: описание идеи
            - target_audience: целевая аудитория
            - investment: инвестиции
            - competition: конкуренты
            - revenue_model: модель дохода
        :return: Результат анализа
        """
        self.weak_points = []
        
        idea = data.get("idea_description", "")
        audience = data.get("target_audience", "")
        competition = data.get("competition", "")
        revenue = data.get("revenue_model", "")
        investment = data.get("investment", "")
        
        # Анализ описания идеи
        self._analyze_idea_description(idea)
        
        # Анализ целевой аудитории
        self._analyze_audience(audience)
        
        # Анализ знания конкурентов
        self._analyze_competition(competition)
        
        # Анализ модели дохода
        self._analyze_revenue_model(revenue)
        
        # Анализ инвестиций
        self._analyze_investment(investment)
        
        # Генерация вердикта
        verdict = self._generate_verdict()
        
        return {
            "verdict": verdict["text"],
            "zone": verdict["zone"],
            "weak_points": self.weak_points,
            "recommendation": self._get_recommendation(verdict["zone"])
        }
    
    def _analyze_idea_description(self, idea: str) -> None:
        """Анализ описания идеи"""
        if len(str(idea)) < 20:
            self.weak_points.append("❌ Идея описана слишком кратко")
    
    def _analyze_audience(self, audience: str) -> None:
        """Анализ описания целевой аудитории"""
        audience_lower = str(audience).lower()
        if "не знаю" in audience_lower or "білмеймін" in audience_lower or len(str(audience)) < 10:
            self.weak_points.append("❌ Клиент не определён")
    
    def _analyze_competition(self, competition: str) -> None:
        """Анализ знания конкурентов"""
        comp_lower = str(competition).lower()
        if "не знаю" in comp_lower or "білмеймін" in comp_lower:
            self.weak_points.append("❌ Конкурентов не изучал")
    
    def _analyze_revenue_model(self, revenue: str) -> None:
        """Анализ модели дохода"""
        if len(str(revenue)) < 10:
            self.weak_points.append("❌ Модель дохода неясна")
    
    def _analyze_investment(self, investment: str) -> None:
        """Анализ инвестиций (заглушка)"""
        # Здесь будет логика анализа адекватности инвестиций
        pass
    
    def _generate_verdict(self) -> Dict:
        """Генерация итогового вердикта"""
        if len(self.weak_points) >= 3:
            return {
                "text": "🔴 Красная зона\n\nИдея сырая. Много неизвестных.",
                "zone": "red"
            }
        elif len(self.weak_points) >= 1:
            return {
                "text": "🟡 Жёлтая зона\n\nИдея имеет право на жизнь.",
                "zone": "yellow"
            }
        else:
            return {
                "text": "🟢 Зелёная зона\n\nИдея проработана хорошо.",
                "zone": "green"
            }
    
    def _get_recommendation(self, zone: str) -> str:
        """Рекомендация по действиям"""
        recommendations = {
            "red": "Идея слишком сырая. Проработайте каждый пункт: клиент, конкуренты, доход.",
            "yellow": "Идея имеет потенциал, но требует доработки. Изучите слабые места.",
            "green": "Идея хорошо проработана. Можно начинать быстрый тест."
        }
        return recommendations.get(zone, "")


def generate_idea_verdict(data: Dict) -> str:
    """
    Генерация вердикта для идеи (для Telegram бота)
    
    :param data: Данные об идее
    :return: Текст вердикта
    """
    generator = IdeaVerdictGenerator()
    result = generator.analyze(data)
    
    verdict_text = result["verdict"]
    
    if result["weak_points"]:
        verdict_text += "\n\n" + "\n".join(result["weak_points"])
    
    return verdict_text
