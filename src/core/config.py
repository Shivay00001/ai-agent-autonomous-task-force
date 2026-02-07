from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    MODEL_NAME: str = "gpt-4-turbo-preview"
    SUPERVISOR_MODEL: str = "gpt-4-turbo-preview"
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

try:
    settings = Settings()
except Exception:
    import os
    class MockSettings:
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "mock_key")
        MODEL_NAME = "gpt-4-turbo-preview"
        SUPERVISOR_MODEL = "gpt-4-turbo-preview"
        LOG_LEVEL = "INFO"
    settings = MockSettings()
