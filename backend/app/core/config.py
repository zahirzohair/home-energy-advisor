from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = "sqlite:///./home_energy.db"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000"

    APP_NAME: str = "Home Energy Advisor"
    VERSION: str = "1.0.0"
    DEBUG: bool = False


settings = Settings()
