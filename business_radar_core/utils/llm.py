"""
LLM Integration for Business Radar Bot
Supports Qwen (Alibaba) and local models via Ollama
"""
import os
from typing import Dict, Optional, List
from loguru import logger


class QwenAnalyzer:
    """
    Бизнес-анализ через Qwen LLM (Alibaba)
    
    Поддержка:
    - Qwen API (dashscope)
    - Локальные модели через Ollama
    - Fallback на rule-based при отсутствии API
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        use_local: bool = False,
        local_model: str = "qwen2.5:7b"
    ):
        """
        Инициализация анализатора
        
        :param api_key: Qwen API ключ (dashscope)
        :param use_local: Использовать локальную модель
        :param local_model: Название локальной модели
        """
        self.api_key = api_key or os.getenv('QWEN_API_KEY')
        self.use_local = use_local or os.getenv('USE_LOCAL_LLM', 'false').lower() == 'true'
        self.local_model = local_model
        self._client = None
        self._ollama_client = None
        
        if self.api_key and not self.use_local:
            self._init_dashscope()
        elif self.use_local:
            self._init_ollama()
    
    def _init_dashscope(self):
        """Инициализация DashScope (Qwen API)"""
        try:
            from dashscope import Generation
            Generation.api_key = self.api_key
            self._client = Generation
            logger.info("Qwen API (dashscope) инициализирован")
        except ImportError:
            logger.warning("dashscope не установлен. Fallback на rule-based.")
            self._client = None
    
    def _init_ollama(self):
        """Инициализация Ollama (локальные модели)"""
        try:
            import ollama
            self._ollama_client = ollama
            logger.info(f"Ollama инициализирован: {self.local_model}")
        except ImportError:
            logger.warning("ollama не установлен. Fallback на rule-based.")
            self._ollama_client = None
    
    def analyze_debt(self, data: Dict) -> Dict:
        """
        Анализ ситуации с долгом
        
        :param data: Данные о долге
        :return: Результат анализа с вердиктом
        """
        prompt = self._create_debt_prompt(data)
        response = self._generate(prompt)
        
        if response:
            return self._parse_debt_response(response)
        
        # Fallback на rule-based
        from business_radar_core.modules.debt import DebtVerdictGenerator
        generator = DebtVerdictGenerator()
        result = generator.analyze(data)
        result["ai_generated"] = False
        return result
    
    def analyze_market(self, data: Dict) -> Dict:
        """
        Анализ рыночной позиции
        
        :param data: Данные о рынке
        :return: Результат анализа
        """
        prompt = self._create_market_prompt(data)
        response = self._generate(prompt)
        
        if response:
            return self._parse_market_response(response)
        
        # Fallback
        from business_radar_core.modules.market import MarketVerdictGenerator
        generator = MarketVerdictGenerator()
        result = generator.analyze(data)
        result["ai_generated"] = False
        return result
    
    def analyze_hiring(self, data: Dict) -> Dict:
        """
        Анализ рисков найма
        
        :param data: Данные о кандидате
        :return: Результат анализа
        """
        prompt = self._create_hiring_prompt(data)
        response = self._generate(prompt)
        
        if response:
            return self._parse_hiring_response(response)
        
        # Fallback
        from business_radar_core.modules.hiring import HiringVerdictGenerator
        generator = HiringVerdictGenerator()
        result = generator.analyze(data)
        result["ai_generated"] = False
        return result
    
    def analyze_import(self, data: Dict) -> Dict:
        """
        Анализ рисков импорта
        
        :param data: Данные об импорте
        :return: Результат анализа
        """
        prompt = self._create_import_prompt(data)
        response = self._generate(prompt)
        
        if response:
            return self._parse_import_response(response)
        
        # Fallback
        from business_radar_core.modules.import_mod import ImportVerdictGenerator
        generator = ImportVerdictGenerator()
        result = generator.analyze(data)
        result["ai_generated"] = False
        return result
    
    def analyze_idea(self, data: Dict) -> Dict:
        """
        Анализ бизнес-идеи
        
        :param data: Данные об идее
        :return: Результат анализа
        """
        prompt = self._create_idea_prompt(data)
        response = self._generate(prompt)
        
        if response:
            return self._parse_idea_response(response)
        
        # Fallback
        from business_radar_core.modules.idea import IdeaVerdictGenerator
        generator = IdeaVerdictGenerator()
        result = generator.analyze(data)
        result["ai_generated"] = False
        return result
    
    def _generate(self, prompt: str) -> Optional[str]:
        """
        Генерация ответа от LLM
        
        :param prompt: Текст запроса
        :return: Ответ модели
        """
        if self.use_local and self._ollama_client:
            return self._generate_ollama(prompt)
        elif self._client:
            return self._generate_dashscope(prompt)
        return None
    
    def _generate_dashscope(self, prompt: str) -> Optional[str]:
        """Генерация через Qwen API"""
        try:
            response = self._client.call(
                model='qwen-turbo',
                prompt=prompt,
                max_tokens=1000,
                temperature=0.3
            )
            return response.output.text
        except Exception as e:
            logger.error(f"Qwen API error: {e}")
            return None
    
    def _generate_ollama(self, prompt: str) -> Optional[str]:
        """Генерация через локальную Ollama модель"""
        try:
            response = self._ollama_client.generate(
                model=self.local_model,
                prompt=prompt,
                stream=False
            )
            return response['response']
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return None
    
    # ========== PROMPTS ==========
    
    def _create_debt_prompt(self, data: Dict) -> str:
        """Создание промпта для анализа долга"""
        return f"""
Ты бизнес-аналитик для предпринимателей Казахстана.
Твоя задача — дать холодный, честный вердикт без эмоций.

Данные о долге:
- Сумма: {data.get('amount', 'не указано')} тенге
- Срок: {data.get('date', 'не указано')}
- Должник: {data.get('debtor_type', 'не указано')}
- Доказательства: {data.get('evidence', 'не указано')}
- Контакт с должником: {data.get('contact_status', 'не указано')}

Формат ответа СТРОГО:
🟢/🟡/🔴 Зона: [название]

Проблемы:
• [проблема 1]
• [проблема 2]

Рекомендации:
• [рекомендация 1]
• [рекомендация 2]

Без воды, только факты. Пиши на русском языке.
"""
    
    def _create_market_prompt(self, data: Dict) -> str:
        """Создание промпта для анализа рынка"""
        return f"""
Ты бизнес-аналитик для предпринимателей Казахстана.

Данные о бизнесе:
- Продукт: {data.get('product', 'не указано')}
- Цена: {data.get('price', 'не указано')} тенге
- Город: {data.get('city', 'не указано')}
- Продажи за месяц: {data.get('sales_volume', 'не указано')} шт
- Конкуренты: {data.get('competitors', 'не указано')}

Дай вердикт: в рынке ли предприниматель?

Формат ответа СТРОГО:
🟢/🟡/🔴 Зона: [название]

Проблемы:
• [проблема 1]

Рекомендации:
• [рекомендация 1]

Пиши на русском языке.
"""
    
    def _create_hiring_prompt(self, data: Dict) -> str:
        """Создание промпта для анализа найма"""
        return f"""
Ты HR-аналитик для предпринимателей Казахстана.

Данные о кандидате:
- Должность: {data.get('position', 'не указано')}
- Опыт: {data.get('experience', 'не указано')}
- Зарплата: {data.get('salary', 'не указано')} тенге
- Рекомендации: {data.get('references', 'не указано')}
- Испытательный срок: {data.get('probation', 'не указано')}

Оцени риски найма.

Формат ответа СТРОГО:
🟢/🟡/🔴 Риск: [уровень]

Флаги:
• [флаг 1]

Рекомендация: [брать/не брать/с осторожностью]

Пиши на русском языке.
"""
    
    def _create_import_prompt(self, data: Dict) -> str:
        """Создание промпта для анализа импорта"""
        return f"""
Ты аналитик ВЭД для предпринимателей Казахстана.

Данные об импорте:
- Товар: {data.get('product_type', 'не указано')}
- Страна: {data.get('country', 'не указано')}
- Партия: {data.get('batch_size', 'не указано')}
- Проверка поставщика: {data.get('supplier_check', 'не указано')}
- Условия оплаты: {data.get('payment_terms', 'не указано')}

Оцени риски импорта.

Формат ответа СТРОГО:
🟢/🟡/🔴 Зона: [название]

Риски:
• [риск 1]

Что проверить до оплаты:
• [проверка 1]

Пиши на русском языке.
"""
    
    def _create_idea_prompt(self, data: Dict) -> str:
        """Создание промпта для анализа идеи"""
        return f"""
Ты бизнес-аналитик для стартапов в Казахстане.

Данные об идее:
- Описание: {data.get('idea_description', 'не указано')}
- Клиент: {data.get('target_audience', 'не указано')}
- Инвестиции: {data.get('investment', 'не указано')} тенге
- Конкуренты: {data.get('competition', 'не указано')}
- Модель дохода: {data.get('revenue_model', 'не указано')}

Найди слабые места идеи.

Формат ответа СТРОГО:
🟢/🟡/🔴 Зона: [название]

Слабые места:
• [слабость 1]

Как проверить быстро:
• [тест 1]

Пиши на русском языке.
"""
    
    # ========== PARSERS ==========
    
    def _parse_debt_response(self, response: str) -> Dict:
        """Парсинг ответа для долга"""
        return {
            "verdict": response,
            "zone": self._extract_zone(response),
            "ai_generated": True
        }
    
    def _parse_market_response(self, response: str) -> Dict:
        """Парсинг ответа для рынка"""
        return {
            "verdict": response,
            "zone": self._extract_zone(response),
            "ai_generated": True
        }
    
    def _parse_hiring_response(self, response: str) -> Dict:
        """Парсинг ответа для найма"""
        return {
            "verdict": response,
            "risk_level": self._extract_zone(response),
            "ai_generated": True
        }
    
    def _parse_import_response(self, response: str) -> Dict:
        """Парсинг ответа для импорта"""
        return {
            "verdict": response,
            "zone": self._extract_zone(response),
            "ai_generated": True
        }
    
    def _parse_idea_response(self, response: str) -> Dict:
        """Парсинг ответа для идеи"""
        return {
            "verdict": response,
            "zone": self._extract_zone(response),
            "ai_generated": True
        }
    
    def _extract_zone(self, text: str) -> str:
        """Извлечение зоны из ответа"""
        if "🟢" in text or "Зелёная" in text or "Низкий" in text:
            return "green"
        elif "🟡" in text or "Жёлтая" in text or "Средний" in text:
            return "yellow"
        elif "🔴" in text or "Красная" in text or "Высокий" in text:
            return "red"
        return "unknown"


# Глобальный экземпляр
analyzer = QwenAnalyzer()
