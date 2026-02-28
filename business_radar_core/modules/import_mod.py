"""
Module 4: Import Risk Assessment (Мүлде кірісу керек пе? / Стоит ли лезть)
Business logic only - no Telegram dependencies
"""
from typing import Dict, List


class ImportVerdictGenerator:
    """
    Генератор вердиктов для модуля импорта
    
    Анализирует риски импорта:
    - 🟢 Зелёная зона: риски минимальные
    - 🟡 Жёлтая зона: есть риски
    - 🔴 Красная зона: очень высокие риски
    """
    
    def __init__(self):
        self.risk_factors: List[str] = []
    
    def analyze(self, data: Dict) -> Dict:
        """
        Анализ рисков импорта
        
        :param data: Словарь с данными:
            - product_type: товар
            - country: страна
            - batch_size: размер партии
            - supplier_check: проверка поставщика
            - payment_terms: условия оплаты
        :return: Результат анализа
        """
        self.risk_factors = []
        
        supplier_check = data.get("supplier_check", "")
        payment = data.get("payment_terms", "")
        country = data.get("country", "")
        batch = data.get("batch_size", "")
        
        # Анализ проверки поставщика
        self._analyze_supplier_check(supplier_check)
        
        # Анализ условий оплаты
        self._analyze_payment_terms(payment)
        
        # Анализ страны
        self._analyze_country(country)
        
        # Анализ размера партии
        self._analyze_batch_size(batch)
        
        # Генерация вердикта
        verdict = self._generate_verdict()
        
        return {
            "verdict": verdict["text"],
            "zone": verdict["zone"],
            "risk_factors": self.risk_factors,
            "recommendation": self._get_recommendation(verdict["zone"])
        }
    
    def _analyze_supplier_check(self, supplier_check: str) -> None:
        """Анализ проверки поставщика"""
        check_lower = str(supplier_check).lower()
        if "не проверял" in check_lower or "тексермедім" in check_lower:
            self.risk_factors.append("🔴 Не проверял поставщика — 90% проблем от этого")
    
    def _analyze_payment_terms(self, payment: str) -> None:
        """Анализ условий оплаты"""
        payment_lower = str(payment).lower()
        if "100%" in payment_lower or "алдын ала" in payment_lower or "предоплата" in payment_lower:
            self.risk_factors.append("🔴 100% предоплата — максимальный риск")
    
    def _analyze_country(self, country: str) -> None:
        """Анализ страны импорта"""
        country_lower = str(country).lower()
        if "китай" in country_lower or "қытай" in country_lower:
            self.risk_factors.append("⚠️ Китай — долгая доставка, возможен брак")
    
    def _analyze_batch_size(self, batch: str) -> None:
        """Анализ размера партии (заглушка)"""
        # Здесь будет логика анализа размера партии
        pass
    
    def _generate_verdict(self) -> Dict:
        """Генерация итогового вердикта"""
        if len(self.risk_factors) >= 3:
            return {
                "text": "🔴 Красная зона\n\nОчень высокие риски.",
                "zone": "red"
            }
        elif len(self.risk_factors) >= 1:
            return {
                "text": "🟡 Жёлтая зона\n\nЕсть риски.",
                "zone": "yellow"
            }
        else:
            return {
                "text": "🟢 Зелёная зона\n\nРиски минимальные.",
                "zone": "green"
            }
    
    def _get_recommendation(self, zone: str) -> str:
        """Рекомендация по действиям"""
        recommendations = {
            "red": "Критические риски! Проверьте поставщика, не платите 100% вперёд.",
            "yellow": "Есть риски, но управляемые. Проверьте поставщика перед оплатой.",
            "green": "Риски минимальные. Можно продолжать, но проверяйте документы."
        }
        return recommendations.get(zone, "")


def generate_import_verdict(data: Dict) -> str:
    """
    Генерация вердикта для импорта (для Telegram бота)
    
    :param data: Данные об импорте
    :return: Текст вердикта
    """
    generator = ImportVerdictGenerator()
    result = generator.analyze(data)
    
    verdict_text = result["verdict"]
    
    if result["risk_factors"]:
        verdict_text += "\n\n" + "\n".join(result["risk_factors"])
    
    return verdict_text
