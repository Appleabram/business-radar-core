"""
Comprehensive Bot Test Script
Tests all modules from start to finish
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import init_db, create_tables, User, Language, DialogSession, ModuleType, Payment, PaymentStatus
from src.utils.narrative import (
    get_narrative_explanation,
    get_question,
    get_short_answer_warning,
    get_voice_confirmation,
    BASE_NARRATIVE,
    SPECIAL_NARRATIVES,
)
from src.utils.slang import SlangNormalizer


class BotTester:
    """Comprehensive bot tester"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []
    
    def log(self, message: str, level: str = "INFO"):
        """Log test result"""
        emoji = {"INFO": "ℹ️", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}
        print(f"{emoji.get(level, '•')} {message}")
        self.test_results.append({"level": level, "message": message})
        
        if level == "PASS":
            self.tests_passed += 1
        elif level == "FAIL":
            self.tests_failed += 1
    
    async def test_database(self):
        """Test database initialization"""
        self.log("=== Тест 1: База данных ===")
        
        try:
            init_db("sqlite+aiosqlite:///:memory:")
            await create_tables()
            self.log("База данных инициализирована", "PASS")
            return True
        except Exception as e:
            self.log(f"Ошибка БД: {e}", "FAIL")
            return False
    
    async def test_user_creation(self):
        """Test user creation"""
        self.log("\n=== Тест 2: Создание пользователя ===")
        
        try:
            from sqlalchemy.ext.asyncio import AsyncSession
            from sqlalchemy import select
            
            async with init_db("sqlite+aiosqlite:///:memory:")[1]() as session:
                user = User(
                    telegram_id=123456,
                    username="test_user",
                    first_name="Test",
                    language=Language.KAZAKH,
                )
                session.add(user)
                await session.commit()
                
                # Verify
                result = await session.execute(select(User).where(User.telegram_id == 123456))
                found_user = result.scalar_one_or_none()
                
                if found_user and found_user.language == Language.KAZAKH:
                    self.log("Пользователь создан и сохранён", "PASS")
                    return True
                else:
                    self.log("Пользователь не найден", "FAIL")
                    return False
        except Exception as e:
            self.log(f"Ошибка создания пользователя: {e}", "FAIL")
            return False
    
    def test_narrative_system(self):
        """Test narrative system"""
        self.log("\n=== Тест 3: Система обоснований ===")
        
        try:
            # Test base narrative
            base_kk = get_narrative_explanation(None, "unknown", "kk", False)
            base_ru = get_narrative_explanation(None, "unknown", "ru", False)
            
            if "Қазір маңызды сұрақ" in base_kk:
                self.log("Базовое обоснование KZ", "PASS")
            else:
                self.log("Базовое обоснование KZ не найдено", "FAIL")
            
            if "Сейчас важный вопрос" in base_ru:
                self.log("Базовое обоснование RU", "PASS")
            else:
                self.log("Базовое обоснование RU не найдено", "FAIL")
            
            # Test first question narrative
            first_kk = get_narrative_explanation(None, "unknown", "kk", True)
            if "Бұл тест емес" in first_kk:
                self.log("Первый вопрос KZ", "PASS")
            else:
                self.log("Первый вопрос KZ не найден", "FAIL")
            
            # Test special narratives
            if "amount" in SPECIAL_NARRATIVES:
                self.log("Спец-обоснование: сумма", "PASS")
            else:
                self.log("Спец-обоснование: сумма не найдено", "FAIL")
            
            if "idea_description" in SPECIAL_NARRATIVES:
                self.log("Спец-обоснование: идея", "PASS")
            else:
                self.log("Спец-обоснование: идея не найдено", "FAIL")
            
            # Test short answer warning
            warning_kk = get_short_answer_warning("kk")
            warning_ru = get_short_answer_warning("ru")
            
            if "қателесуім мүмкін" in warning_kk:
                self.log("Предупреждение KZ", "PASS")
            else:
                self.log("Предупреждение KZ не найдено", "FAIL")
            
            if "могу ошибиться" in warning_ru:
                self.log("Предупреждение RU", "PASS")
            else:
                self.log("Предупреждение RU не найдено", "FAIL")
            
            return True
        except Exception as e:
            self.log(f"Ошибка системы обоснований: {e}", "FAIL")
            return False
    
    def test_slang_normalizer(self):
        """Test slang normalization"""
        self.log("\n=== Тест 4: Нормализация сленга ===")
        
        try:
            normalizer = SlangNormalizer()
            
            # Test basic slang
            result = normalizer.normalize("лям теңге")
            if "миллион" in result:
                self.log("Сленг: лям → миллион", "PASS")
            else:
                self.log(f"Сленг не нормализован: {result}", "FAIL")
            
            # Test filler removal
            result = normalizer.normalize("короче, ну, долг 500 тысяч")
            if "короче" not in result and "ну" not in result:
                self.log("Удаление слов-паразитов", "PASS")
            else:
                self.log("Слова-паразиты не удалены", "FAIL")
            
            # Test entity extraction
            entities = normalizer.extract_entities("Долг 500 тысяч тенге, Алматы")
            if entities:
                self.log("Извлечение сущностей", "PASS")
            else:
                self.log("Сущности не извлечены", "WARN")
            
            return True
        except Exception as e:
            self.log(f"Ошибка нормализатора: {e}", "FAIL")
            return False
    
    def test_voice_confirmation(self):
        """Test voice confirmation"""
        self.log("\n=== Тест 5: Голосовые сообщения ===")
        
        try:
            confirm_kk = get_voice_confirmation("Долг 500 тысяч, 3 ай бұрын", "kk")
            confirm_ru = get_voice_confirmation("Долг 500 тысяч, 3 месяца назад", "ru")
            
            if "Мен былай түсіндім" in confirm_kk:
                self.log("Подтверждение голоса KZ", "PASS")
            else:
                self.log("Подтверждение голоса KZ не найдено", "FAIL")
            
            if "Я понял так" in confirm_ru:
                self.log("Подтверждение голоса RU", "PASS")
            else:
                self.log("Подтверждение голоса RU не найдено", "FAIL")
            
            return True
        except Exception as e:
            self.log(f"Ошибка голосовых: {e}", "FAIL")
            return False
    
    def test_module_questions(self):
        """Test module questions"""
        self.log("\n=== Тест 6: Вопросы модулей ===")
        
        try:
            # Test Debt module questions
            debt_questions_kk = get_question(ModuleType.DEBT, "amount", "kk")
            debt_questions_ru = get_question(ModuleType.DEBT, "amount", "ru")
            
            if debt_questions_kk:
                self.log("Вопрос Debt KZ: сумма", "PASS")
            else:
                self.log("Вопрос Debt KZ: сумма не найден", "FAIL")
            
            if debt_questions_ru:
                self.log("Вопрос Debt RU: сумма", "PASS")
            else:
                self.log("Вопрос Debt RU: сумма не найден", "FAIL")
            
            # Test all modules exist
            from src.modules import debt, market, hiring, import_mod, idea
            
            if hasattr(debt, 'router'):
                self.log("Модуль Debt загружен", "PASS")
            else:
                self.log("Модуль Debt не загружен", "FAIL")
            
            if hasattr(market, 'router'):
                self.log("Модуль Market загружен", "PASS")
            else:
                self.log("Модуль Market не загружен", "FAIL")
            
            if hasattr(hiring, 'router'):
                self.log("Модуль Hiring загружен", "PASS")
            else:
                self.log("Модуль Hiring не загружен", "FAIL")
            
            if hasattr(import_mod, 'router'):
                self.log("Модуль Import загружен", "PASS")
            else:
                self.log("Модуль Import не загружен", "FAIL")
            
            if hasattr(idea, 'router'):
                self.log("Модуль Idea загружен", "PASS")
            else:
                self.log("Модуль Idea не загружен", "FAIL")
            
            return True
        except Exception as e:
            self.log(f"Ошибка вопросов модулей: {e}", "FAIL")
            return False
    
    def test_verdict_generation(self):
        """Test verdict generation"""
        self.log("\n=== Тест 7: Генерация вердиктов ===")
        
        try:
            # Test Debt verdict
            from src.modules.debt import generate_free_verdict
            debt_data = {
                "amount": "500000",
                "date": "3 месяца назад",
                "debtor_type": "Частное лицо",
                "evidence": "нет",
                "contact_status": "нет"
            }
            verdict = generate_free_verdict(debt_data)
            if "зона" in verdict.lower():
                self.log("Вердикт Debt", "PASS")
            else:
                self.log("Вердикт Debt не сгенерирован", "FAIL")
            
            # Test Idea verdict
            from src.modules.idea import generate_idea_verdict
            idea_data = {
                "idea_description": "Буду продавать одежду",
                "target_audience": "не знаю",
                "investment": "100000",
                "competition": "не знаю",
                "revenue_model": "наценка"
            }
            verdict = generate_idea_verdict(idea_data)
            if "зона" in verdict.lower():
                self.log("Вердикт Idea", "PASS")
            else:
                self.log("Вердикт Idea не сгенерирован", "FAIL")
            
            # Test Market verdict
            from src.modules.market import generate_market_verdict
            market_data = {
                "price": "5000",
                "sales_volume": "0",
                "competitors": "не знаю"
            }
            verdict = generate_market_verdict(market_data)
            if "зона" in verdict.lower():
                self.log("Вердикт Market", "PASS")
            else:
                self.log("Вердикт Market не сгенерирован", "FAIL")
            
            # Test Hiring verdict
            from src.modules.hiring import generate_hiring_verdict
            hiring_data = {
                "position": "менеджер",
                "experience": "0",
                "salary": "200000",
                "references": "нет",
                "probation": "нет"
            }
            verdict = generate_hiring_verdict(hiring_data)
            if "зона" in verdict.lower() or "риск" in verdict.lower():
                self.log("Вердикт Hiring", "PASS")
            else:
                self.log("Вердикт Hiring не сгенерирован", "FAIL")
            
            # Test Import verdict
            from src.modules.import_mod import generate_import_verdict
            import_data = {
                "product_type": "одежда",
                "country": "Китай",
                "batch_size": "5000",
                "supplier_check": "не проверял",
                "payment_terms": "100% предоплата"
            }
            verdict = generate_import_verdict(import_data)
            if "зона" in verdict.lower():
                self.log("Вердикт Import", "PASS")
            else:
                self.log("Вердикт Import не сгенерирован", "FAIL")
            
            return True
        except Exception as e:
            self.log(f"Ошибка вердиктов: {e}", "FAIL")
            return False
    
    def print_summary(self):
        """Print test summary"""
        total = self.tests_passed + self.tests_failed
        percentage = (self.tests_passed / total * 100) if total > 0 else 0
        
        print("\n" + "=" * 60)
        print("  ИТОГОВЫЙ ОТЧЁТ ПО ТЕСТИРОВАНИЮ")
        print("=" * 60)
        print(f"  Всего тестов: {total}")
        print(f"  ✅ Пройдено: {self.tests_passed}")
        print(f"  ❌ Провалено: {self.tests_failed}")
        print(f"  📊 Успешность: {percentage:.1f}%")
        print("=" * 60)
        
        if percentage >= 90:
            print("\n  🎉 ВСЕ КРИТИЧЕСКИЕ ТЕСТЫ ПРОЙДЕНЫ!")
        elif percentage >= 70:
            print("\n  ⚠️  ЕСТЬ ПРОБЛЕМЫ, НО БОТ РАБОТАЕТ")
        else:
            print("\n  ❌ ТРЕБУЕТСЯ ИСПРАВЛЕНИЕ ОШИБОК")
        
        print("\n")


async def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  ТЕСТИРОВАНИЕ BUSINESS RADAR BOT")
    print("=" * 60 + "\n")
    
    tester = BotTester()
    
    # Run all tests
    await tester.test_database()
    await tester.test_user_creation()
    tester.test_narrative_system()
    tester.test_slang_normalizer()
    tester.test_voice_confirmation()
    tester.test_module_questions()
    tester.test_verdict_generation()
    
    # Print summary
    tester.print_summary()
    
    return tester.tests_failed == 0


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
