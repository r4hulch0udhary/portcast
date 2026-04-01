from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")
    test_database_url: str = Field(alias="TEST_DATABASE_URL")
    sqlalchemy_track_modifications: bool = False
    debug: bool = Field(default=False, alias="FLASK_DEBUG")
    env: str = Field(default="production", alias="FLASK_ENV")
    port: int = Field(default=8000, alias="PORT")
    host: str = Field(default="0.0.0.0", alias="HOST")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Config()
