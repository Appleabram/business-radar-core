"""
Basic tests for Business Radar Bot
"""
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.database import Base, User, Language, DialogSession, ModuleType
from src.utils.slang import SlangNormalizer


@pytest.fixture
async def db_session():
    """
    Создать тестовую сессию БД (in-memory SQLite)
    """
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()


@pytest.mark.asyncio
async def test_user_creation(db_session):
    """
    Тест создания пользователя
    """
    user = User(
        telegram_id=123456,
        username="test_user",
        first_name="Test",
        language=Language.KAZAKH,
    )
    
    db_session.add(user)
    await db_session.commit()
    
    assert user.id is not None
    assert user.telegram_id == 123456
    assert user.language == Language.KAZAKH


@pytest.mark.asyncio
async def test_dialog_session(db_session):
    """
    Тест сессии диалога
    """
    # Создать пользователя
    user = User(
        telegram_id=123456,
        username="test_user",
        language=Language.RUSSIAN,
    )
    db_session.add(user)
    await db_session.commit()
    
    # Создать сессию
    session = DialogSession(
        user_id=user.id,
        module=ModuleType.DEBT,
        current_state="amount",
        collected_data={"amount": "500000"},
    )
    db_session.add(session)
    await db_session.commit()
    
    assert session.module == ModuleType.DEBT
    assert session.collected_data["amount"] == "500000"


def test_slang_normalizer_basic():
    """
    Тест нормализации сленга
    """
    normalizer = SlangNormalizer()
    
    # Тест замены сленга
    assert normalizer.normalize("лям") == "миллион"
    assert normalizer.normalize("теңге") == "тенге"
    assert normalizer.normalize("тыс") == "тысяч"


def test_slang_normalizer_entities():
    """
    Тест извлечения сущностей
    """
    normalizer = SlangNormalizer()
    
    text = "Долг 500 тысяч тенге, Алматы"
    entities = normalizer.extract_entities(text)
    
    assert "amounts" in entities or "cities" in entities


def test_slang_normalizer_fillers():
    """
    Тест удаления слов-паразитов
    """
    normalizer = SlangNormalizer()
    
    text = "Короче, ну, типа, долг 500 тысяч"
    normalized = normalizer.normalize(text)
    
    assert "короче" not in normalized
    assert "ну" not in normalized
    assert "типа" not in normalized


@pytest.mark.asyncio
async def test_payment_creation(db_session):
    """
    Тест создания платежа
    """
    from src.database import Payment, PaymentStatus
    
    # Создать пользователя
    user = User(
        telegram_id=123456,
        language=Language.RUSSIAN,
    )
    db_session.add(user)
    await db_session.commit()
    
    # Создать платёж
    payment = Payment(
        user_id=user.id,
        amount_kzt=5000,
        status=PaymentStatus.PENDING,
    )
    db_session.add(payment)
    await db_session.commit()
    
    assert payment.status == PaymentStatus.PENDING
    assert payment.amount_kzt == 5000
