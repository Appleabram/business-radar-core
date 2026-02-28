"""
Module 3: Hiring Risk Assessment (Адам алуға қорқамын / Боюсь брать людей)
Business logic only - no Telegram dependencies
"""
from typing import Dict, List


class HiringVerdictGenerator:
    """
    Генератор вердиктов для модуля найма
    
    Анализирует риски кандидата:
    - 🟢 Низкий риск
    - 🟡 Средний риск
    - 🔴 Высокий риск
    """
    
    def __init__(self):
        self.risk_factors: List[str] = []
    
    def analyze(self, data: Dict) -> Dict:
        """
        Анализ рисков кандидата
        
        :param data: Словарь с данными:
            - position: должность
            - experience: опыт
            - salary: зарплата
            - references: рекомендации
            - probation: испытательный срок
        :return: Результат анализа
        """
        self.risk_factors = []
        
        experience = data.get("experience", "")
        references = data.get("references", "")
        probation = data.get("probation", "")
        salary = data.get("salary", "")
        
        # Анализ опыта
        self._analyze_experience(experience)
        
        # Анализ рекомендаций
        self._analyze_references(references)
        
        # Анализ испытательного срока
        self._analyze_probation(probation)
        
        # Анализ зарплаты
        self._analyze_salary(salary)
        
        # Генерация вердикта
        verdict = self._generate_verdict()
        
        return {
            "verdict": verdict["text"],
            "risk_level": verdict["level"],
            "risk_factors": self.risk_factors,
            "recommendation": self._get_recommendation(verdict["level"])
        }
    
    def _analyze_experience(self, experience: str) -> None:
        """Анализ опыта работы"""
        exp_lower = str(experience).lower()
        if "без" in exp_lower or "тәжірибесіз" in exp_lower or experience == "0":
            self.risk_factors.append("❌ Нет опыта — высокий риск ошибок")
    
    def _analyze_references(self, references: str) -> None:
        """Анализ рекомендаций"""
        ref_lower = str(references).lower()
        if "нет" in ref_lower or "жоқ" in ref_lower:
            self.risk_factors.append("❌ Нет рекомендаций — красный флаг")
    
    def _analyze_probation(self, probation: str) -> None:
        """Анализ испытательного срока"""
        prob_lower = str(probation).lower()
        if "нет" in prob_lower or "жоқ" in prob_lower:
            self.risk_factors.append("⚠️ Нет испытательного срока — риск ошибки при найме")
    
    def _analyze_salary(self, salary: str) -> None:
        """Анализ ожидаемой зарплаты (заглушка)"""
        # Здесь будет логика сравнения с рынком
        pass
    
    def _generate_verdict(self) -> Dict:
        """Генерация итогового вердикта"""
        if len(self.risk_factors) >= 3:
            return {
                "text": "🔴 Высокий риск\n\nКандидат опасен.",
                "level": "high"
            }
        elif len(self.risk_factors) >= 1:
            return {
                "text": "🟡 Средний риск\n\nЕсть риски.",
                "level": "medium"
            }
        else:
            return {
                "text": "🟢 Низкий риск\n\nКандидат выглядит надёжно.",
                "level": "low"
            }
    
    def _get_recommendation(self, level: str) -> str:
        """Рекомендация по найму"""
        recommendations = {
            "high": "Рекомендую отказаться. Слишком много красных флагов.",
            "medium": "Можно рассмотреть, но с осторожностью. Введите испытательный срок.",
            "low": "Кандидат выглядит надёжно. Можно предлагать оффер."
        }
        return recommendations.get(level, "")


def generate_hiring_verdict(data: Dict) -> str:
    """
    Генерация вердикта для найма (для Telegram бота)
    
    :param data: Данные о кандидате
    :return: Текст вердикта
    """
    generator = HiringVerdictGenerator()
    result = generator.analyze(data)
    
    verdict_text = result["verdict"]
    
    if result["risk_factors"]:
        verdict_text += "\n\n" + "\n".join(result["risk_factors"])
    
    return verdict_text
