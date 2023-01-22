import httpx
from config.config import CONFIG


async def verification_email(email: str) -> str:
    """Checks the correctness of the email address"""
    url = f'https://api.hunter.io/v2/email-verifier'
    try:
        result = httpx.get(url=url, params={'email': email, 'api_key': CONFIG.HUNTER_API_KEY})
        return result.json()['data']['status']
    except Exception as e:
        raise e
