# config.py
# Central configuration using environment variables.
# Works for both local development and production.

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Environment
    environment: str = "development"

    # LLM Provider
    llm_provider: str = "groq"

    # Groq settings (production)
    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.3-70b-versatile"

    # Ollama settings (local dev fallback)
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.2:1b"

    # HuggingFace (optional)
    huggingface_token: Optional[str] = None

    # Database (optional for MVP)
    database_url: Optional[str] = None

    # Session
    session_expiry_minutes: int = 60
    secret_key: str = "change-this-in-production"

    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    # Frontend URL (set in production)
    frontend_url: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()