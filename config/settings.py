"""Configuration Settings"""
from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application Settings"""
    
    # API
    APP_NAME: str = "Helmet Detection System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///astra.db")
    
    # AI/ML
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Model Config
    YOLO_MODEL_SIZE: str = os.getenv("YOLO_MODEL_SIZE", "n")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.70"))
    NMS_THRESHOLD: float = float(os.getenv("NMS_THRESHOLD", "0.45"))
    
    # Video Processing
    MAX_VIDEO_SIZE_MB: int = int(os.getenv("MAX_VIDEO_SIZE_MB", "100"))
    FRAMES_PER_SECOND: int = int(os.getenv("FRAMES_PER_SECOND", "5"))
    PROCESS_TIMEOUT_MINUTES: int = int(os.getenv("PROCESS_TIMEOUT_MINUTES", "15"))
    
    # Storage
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", "./data")
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "./logs/astra.log")
    
    # Allowed formats
    ALLOWED_FORMATS: set = {"mp4", "avi", "mov", "mkv"}
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
