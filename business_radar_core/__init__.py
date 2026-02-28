"""
Business Radar Core
Ядро диагностических модулей для предпринимателей Казахстана
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from business_radar_core.modules import debt, market, hiring, import_mod, idea
from business_radar_core.utils import narrative, slang
from business_radar_core.locales import kk, ru
from business_radar_core.models import user

__all__ = [
    "debt",
    "market",
    "hiring",
    "import_mod",
    "idea",
    "narrative",
    "slang",
    "kk",
    "ru",
    "user",
]
