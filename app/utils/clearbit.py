import clearbit
from config.config import CONFIG
from typing import Optional


async def get_clearbit_data(email: str) -> Optional[dict]:
    """Get Clearbit user data"""
    clearbit.key = CONFIG.CLEARBIT_API_KEY
    try:
        return clearbit.Enrichment.find(email=email)
    except Exception as e:
        pass
