"""
User model for Business Radar Bot
"""
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Language(str, Enum):
    """Supported languages"""
    KAZAKH = "kk"
    RUSSIAN = "ru"


class User:
    """
    User profile model
    
    Note: This is a simplified model for documentation.
    Full SQLAlchemy model is in the private bot repository.
    """
    
    def __init__(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        language: Language = Language.KAZAKH,
    ):
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.language = language
        self.is_premium = False
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def __repr__(self) -> str:
        return f"User(telegram_id={self.telegram_id}, language={self.language})"
