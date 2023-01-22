from pydantic import BaseSettings
import os


class Config(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    HUNTER_API_KEY: str
    CLEARBIT_API_KEY: str

    class Config:
        env_file = f'{os.getcwd()}/.env'

CONFIG = Config()
