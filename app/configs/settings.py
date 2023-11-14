from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

@lru_cache()
def get_settings():
    return Settings()

class Settings(BaseSettings):
    BASE_MODEL_PATH: str
    LORA_MODEL_PATH: str
    FOLDER_TOKENIZER_PATH: str
    DATASET_BASE_PATH: str
    TAGGERS_BASE_PATH: str
    BITS: int
    GPU_INDEX: int = 0
    FN_OUT_TSV: str = ""

    model_config = SettingsConfigDict(env_file="./app/config/settings.env")