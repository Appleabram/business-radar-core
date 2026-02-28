"""
Module 1: Debt Recovery (Маған қарыз / Мне должны)
Business logic only - no Telegram dependencies
"""
from typing import Dict, List


class DebtVerdictGenerator:
    """
    Генератор вердиктов для модуля долгов
    
    Анализирует данные о долге и определяет зону риска:
    - 🟢 Зелёная: хорошие шансы на возврат
    - 🟡 Жёлтая: риски 50/50
    - 🔴 Красная: низкие шансы на возврат
    """
    
    def __init__(self):
        self.risk_factors: List[str] = []
    
    def analyze(self, data: Dict) -> Dict:
        """
        Анализ данных о долге
        
        :param data: Словарь с данными:
            - amount: сумма долга
            - date: когда возник долг
            - debtor_type: тип должника
            - evidence: доказательства
            - contact_status: статус контакта
        :return: Результат анализа с вердиктом
        """
        self.risk_factors = []
        
        amount = data.get("amount", "0")
        date = data.get("date", "")
        debtor_type = data.get("debtor_type", "")
        evidence = data.get("evidence", "")
        contact = data.get("contact_status", "")
        
        # Анализ суммы
        self._analyze_amount(amount)
        
        # Анализ срока
        self._analyze_date(date)
        
        # Анализ типа должника
        self._analyze_debtor_type(debtor_type)
        
        # Анализ доказательств
        self._analyze_evidence(evidence)
        
        # Анализ контакта
        self._analyze_contact(contact)
        
        # Генерация вердикта
        verdict = self._generate_verdict()
        
        return {
            "verdict": verdict["text"],
            "zone": verdict["zone"],
            "risk_factors": self.risk_factors,
            "recommendation": self._get_recommendation(verdict["zone"])
        }
    
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
            return {
                "text": "🔴 Красная зона\n\nШансы на возврат низкие.",
                "zone": "red"
            }
        elif len(self.risk_factors) >= 1:
            return {
                "text": "🟡 Жёлтая зона\n\nШансы 50/50.",
                "zone": "yellow"
            }
        else:
            return {
                "text": "🟢 Зелёная зона\n\nХорошие шансы на возврат.",
                "zone": "green"
            }
    
    def _get_recommendation(self, zone: str) -> str:
        """Рекомендация по действиям"""
        recommendations = {
            "red": "Рекомендую обратиться к юристу. Шансы низкие, но попробовать стоит.",
            "yellow": "Можно попробовать вернуть самостоятельно. Начните с официальной претензии.",
            "green": "Высокие шансы на возврат. Начните с переговоров, затем претензия."
        }
        return recommendations.get(zone, "")


def generate_free_verdict(data: Dict) -> str:
    """
    Генерация бесплатного вердикта (для Telegram бота)
    
    :param data: Данные о долге
    :return: Текст вердикта
    """
    generator = DebtVerdictGenerator()
    result = generator.analyze(data)
    
    verdict_text = result["verdict"]
    
    if result["risk_factors"]:
        verdict_text += "\n\nПроблемы:\n• " + "\n• ".join(result["risk_factors"])
    
    return verdict_text
