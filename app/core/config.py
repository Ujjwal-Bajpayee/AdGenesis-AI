import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    PROJECT_NAME: str = "AdGenesis AI"
    API_V1_STR: str = "/api/v1"
    
    LLM_PROVIDER: str = Field(default="gemini", description="LLM provider: gemini, openai, openrouter, ollama")
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API Key")
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API Key")
    OPENAI_API_BASE: str = Field(default="https://api.openai.com/v1", description="OpenAI API Base URL")
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434", description="Ollama API Base URL")
    LLM_MODEL_NAME: str = Field(default="gemini-1.5-flash", description="Model name to use")
    
    MONGODB_URL: str = Field(default="mongodb://localhost:27017", description="MongoDB connection URL")
    MONGODB_DATABASE: str = Field(default="adgenesis_ai", description="MongoDB database name")
    
    STORAGE_DIR: str = Field(default="./storage_data", description="Local directory for video and frame storage")
    
    EMBEDDING_MODEL_NAME: str = Field(default="all-MiniLM-L6-v2", description="Sentence Transformers model name")
    
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

settings = Settings()
