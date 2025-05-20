from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()


class ConfigSetting(BaseSettings):

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    LEADERBOARD_REDIS_CHANNEL: str

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return ConfigSetting()

settings = get_settings()