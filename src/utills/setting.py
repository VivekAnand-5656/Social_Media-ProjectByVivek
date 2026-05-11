from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",extra="ignore")
    DATABASE_URL : str
    SECRET_KEY : str
    ALGORITHM  : str
    EXP_TIME : int

    CLOUD_NAME : str
    API_KEY : str
    API_SECRET : str

setting = Settings()
print(setting.DATABASE_URL)