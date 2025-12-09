from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AlgoPilot API"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    LLM_BASE_URL: str
    LLM_API_KEY: str = "dummy-key"
    LLM_DEFAULT_MODEL: str = "gpt-oss-120b"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()