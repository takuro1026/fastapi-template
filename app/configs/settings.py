from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

@lru_cache()
def get_settings():
    return Settings()

class Settings(BaseSettings):
    SOMETHING_KEY: str
    SOMETHING_PATH: str


    model_config = SettingsConfigDict(env_file='./app/config/settings.env')