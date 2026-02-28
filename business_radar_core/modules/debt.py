"""
Module 1: Debt Recovery (Маған қарыз / Мне должны)
Business logic with AI-powered verdicts
"""
from typing import Dict, List, Optional
from business_radar_core.utils.llm import QwenAnalyzer


class DebtVerdictGenerator:
    """
    Генератор вердиктов для модуля долгов
    
    Поддерживает:
    - Rule-based анализ (базовый)
    - AI анализ через Qwen (опционально)
    """
    
    def __init__(self, use_ai: bool = False, analyzer: Optional[QwenAnalyzer] = None):
        self.risk_factors: List[str] = []
        self.use_ai = use_ai
        self.analyzer = analyzer or QwenAnalyzer()
    
    def analyze(self, data: Dict) -> Dict:
        """
        Анализ данных о долге
        
        :param data: Словарь с данными о долге
        :return: Результат анализа с вердиктом
        """
        # Если включен AI и анализатор доступен
        if self.use_ai and self.analyzer:
            try:
                ai_result = self.analyzer.analyze_debt(data)
                if ai_result.get("ai_generated"):
                    return ai_result
            except Exception as e:
                # Fallback на rule-based при ошибке AI
                pass
        
        # Rule-based анализ
        self.risk_factors = []
        self._analyze_all(data)
        verdict = self._generate_verdict()
        
        return {
            "verdict": verdict["text"],
            "zone": verdict["zone"],
            "risk_factors": self.risk_factors,
            "recommendation": self._get_recommendation(verdict["zone"]),
            "ai_generated": False
        }
    
    def _analyze_all(self, data: Dict) -> None:
        """Запуск всех анализов"""
        self._analyze_amount(data.get("amount", "0"))
        self._analyze_date(data.get("date", ""))
        self._analyze_debtor_type(data.get("debtor_type", ""))
        self._analyze_evidence(data.get("evidence", ""))
        self._analyze_contact(data.get("contact_status", ""))
    
    def _analyze_amount(self, amount: str) -> None:
        """Анализ суммы долга"""
        try:
            amount_num = float(str(amount).replace(" ", "").replace(",", ""))
            if amount_num < 100000:
                self.risk_factors.append("Сумма небольшая — стоит ли тратить время?")
            elif amount_num > 5000000:
                self.risk_factors.append("Крупная сумма — рекомендую юриста.")
        except (ValueError, TypeError):
            pass
    
    def _analyze_date(self, date: str) -> None:
        """Анализ срока долга"""
        date_lower = str(date).lower()
        if "год" in date_lower or "лет" in date_lower:
            self.risk_factors.append("Долг старый — высокий риск невозврата.")
        elif "месяц" in date_lower:
            self.risk_factors.append("Срок средний — ещё можно вернуть.")
    
    def _analyze_debtor_type(self, debtor_type: str) -> None:
        """Анализ типа должника"""
        if debtor_type == "Неизвестно" or debtor_type == "Белгісіз":
            self.risk_factors.append("Должник исчез — это плохой знак.")
        elif debtor_type == "Частное лицо" or debtor_type == "Жеке тұлға":
            self.risk_factors.append("С физлиц взыскать сложнее, чем с юрлиц.")
    
    def _analyze_evidence(self, evidence: str) -> None:
        """Анализ доказательств"""
        evidence_lower = str(evidence).lower()
        if "нет" in evidence_lower or "жоқ" in evidence_lower or "не знаю" in evidence_lower:
            self.risk_factors.append("Нет доказательств — позиция слабая.")
    
    def _analyze_contact(self, contact: str) -> None:
        """Анализ контакта с должником"""
        contact_lower = str(contact).lower()
        if "нет" in contact_lower or "не выходит" in contact_lower or "жоқ" in contact_lower:
            self.risk_factors.append("Не выходит на связь — готовьтесь к суду.")
    
    def _generate_verdict(self) -> Dict:
        """Генерация итогового вердикта"""
        if len(self.risk_factors) >= 3:
            return {"text": "🔴 Красная зона\n\nШансы на возврат низкие.", "zone": "red"}
        elif len(self.risk_factors) >= 1:
            return {"text": "🟡 Жёлтая зона\n\nШансы 50/50.", "zone": "yellow"}
        else:
            return {"text": "🟢 Зелёная зона\n\nХорошие шансы на возврат.", "zone": "green"}
    
    def _get_recommendation(self, zone: str) -> str:
        """Рекомендация по действиям"""
        recommendations = {
            "red": "Рекомендую обратиться к юристу. Шансы низкие, но попробовать стоит.",
            "yellow": "Можно попробовать вернуть самостоятельно. Начните с официальной претензии.",
            "green": "Высокие шансы на возврат. Начните с переговоров, затем претензия."
        }
        return recommendations.get(zone, "")


def generate_free_verdict(data: Dict, use_ai: bool = False) -> str:
    """
    Генерация бесплатного вердикта
    
    :param data: Данные о долге
    :param use_ai: Использовать AI
    :return: Текст вердикта
    """
    generator = DebtVerdictGenerator(use_ai=use_ai)
    result = generator.analyze(data)
    
    verdict_text = result["verdict"]
    
    if not result.get("ai_generated") and result["risk_factors"]:
        verdict_text += "\n\nПроблемы:\n• " + "\n• ".join(result["risk_factors"])
    
    return verdict_text
