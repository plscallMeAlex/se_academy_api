# This file use for setting the environment variables in .env file
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    # Database
    DB_URL:str

    # Token
    SECRET_KEY:str
    EXPIRE_TIME_HOURS:int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)


# This will cache the settings because it's use a lot
@lru_cache()
def get_settings() -> Setting:
    return Setting()