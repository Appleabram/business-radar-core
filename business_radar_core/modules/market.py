"""
Module 2: Market Analysis (Мен нарықтамын ба? / Я в рынке?)
Business logic only - no Telegram dependencies
"""
from typing import Dict, List


class MarketVerdictGenerator:
    """
    Генератор вердиктов для модуля рынка
    
    Анализирует позицию на рынке и определяет зону:
    - 🟢 Зелёная: нормальная позиция
    - 🟡 Жёлтая: есть риски
    - 🔴 Красная: опасная позиция
    """
    
    def __init__(self):
        self.issues: List[str] = []
    
    def analyze(self, data: Dict) -> Dict:
        """
        Анализ рыночной позиции
        
        :param data: Словарь с данными:
            - product: что продаёшь
            - price: цена
            - city: город
            - sales_volume: объём продаж
            - competitors: конкуренты
        :return: Результат анализа
        """
        self.issues = []
        
        sales = data.get("sales_volume", "0")
        competitors = data.get("competitors", "")
        price = data.get("price", "0")
        
        # Анализ продаж
        self._analyze_sales(sales)
        
        # Анализ конкурентов
        self._analyze_competitors(competitors)
        
        # Анализ цены
        self._analyze_price(price)
        
        # Генерация вердикта
        verdict = self._generate_verdict()
        
        return {
            "verdict": verdict["text"],
            "zone": verdict["zone"],
            "issues": self.issues,
            "recommendation": self._get_recommendation(verdict["zone"])
        }
    
    def _analyze_sales(self, sales: str) -> None:
        """Анализ объёма продаж"""
        try:
            sales_num = int(str(sales).replace(" ", "").replace(",", ""))
            if sales_num == 0:
                self.issues.append("❌ Продаж нет — проблема может быть в цене или канале")
        except (ValueError, TypeError):
            pass
    
    def _analyze_competitors(self, competitors: str) -> None:
        """Анализ знания конкурентов"""
        competitors_lower = str(competitors).lower()
        if "не знаю" in competitors_lower or "білмеймін" in competitors_lower:
            self.issues.append("❌ Конкурентов не изучил — не можешь позиционироваться")
    
    def _analyze_price(self, price: str) -> None:
        """Анализ цены (заглушка для будущей логики)"""
        # Здесь будет логика сравнения с рынком
        pass
    
    def _generate_verdict(self) -> Dict:
        """Генерация итогового вердикта"""
        if len(self.issues) >= 2:
            return {
                "text": "🔴 Красная зона\n\nПозиция опасная.",
                "zone": "red"
            }
        elif len(self.issues) >= 1:
            return {
                "text": "🟡 Жёлтая зона\n\nЕсть риски.",
                "zone": "yellow"
            }
        else:
            return {
                "text": "🟢 Зелёная зона\n\nПозиция на рынке нормальная.",
                "zone": "green"
            }
    
    def _get_recommendation(self, zone: str) -> str:
        """Рекомендация по действиям"""
        recommendations = {
            "red": "Срочно изучите конкурентов и пересмотрите цену. Продаж нет не просто так.",
            "yellow": "Изучите конкурентов и сравните цены. Возможно, вы не в рынке.",
            "green": "Позиция нормальная. Продолжайте мониторить рынок и конкурентов."
        }
        return recommendations.get(zone, "")


def generate_market_verdict(data: Dict) -> str:
    """
    Генерация вердикта для рынка (для Telegram бота)
    
    :param data: Данные о рынке
    :return: Текст вердикта
    """
    generator = MarketVerdictGenerator()
    result = generator.analyze(data)
    
    verdict_text = result["verdict"]
    
    if result["issues"]:
        verdict_text += "\n\n" + "\n".join(result["issues"])
    
    return verdict_text
