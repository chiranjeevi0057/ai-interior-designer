# config.py

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    
    # AI Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:1b"
    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.3-70b-versatile"
    llm_provider: str = "groq"

    # Database
    database_url: str
    supabase_url: Optional[str] = None
    supabase_anon_key: Optional[str] = None
    supabase_service_key: Optional[str] = None
    
    # HuggingFace
    huggingface_token: Optional[str] = None
    huggingface_space_url: Optional[str] = None
    
    # App Settings
    secret_key: str = "change-this-in-production"
    environment: str = "development"
    session_expiry_minutes: int = 60
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    frontend_url: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore" 

# Create one single instance used everywhere in the app
settings = Settings()