"""
Configuration management for the SPS Auth Workflow application.

Loads settings from environment variables with sensible defaults.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""
    
    # Flask settings
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    
    # Database settings
    DATABASE_PATH = os.getenv("DATABASE_PATH", "backend/data/sps_auth.db")
