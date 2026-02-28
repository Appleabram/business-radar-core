"""
Diagnostic modules for Business Radar Bot

Each module supports:
- Rule-based analysis (default)
- AI-powered analysis via Qwen (optional)
"""

from business_radar_core.modules import debt, market, hiring, import_mod, idea

__all__ = ["debt", "market", "hiring", "import_mod", "idea"]
