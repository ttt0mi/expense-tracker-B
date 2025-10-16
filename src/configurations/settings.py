from datetime import timedelta
from functools import lru_cache

from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


env_path = find_dotenv()

class Settings(BaseSettings):
	"""pydantic settings used to load environmental variables from env file. not required, use os.getenv() as easier alternative"""
	model_config = SettingsConfigDict(
			env_file=env_path, env_file_encoding="utf-8", extra="ignore", env_ignore_empty=True
	)

	DATABASE_URI: str
	DATABASE_NAME: str
	FLASK_KEY: str
	JWT_KEY: str
	JWT_ACCESS_TOKEN_EXPIRES: int
	JWT_REFRESH_TOKEN_EXPIRES: int
	JWT_ALGORITHM: str



@lru_cache
def get_settings() -> Settings:
	settings = Settings()
	return settings