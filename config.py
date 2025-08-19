"""
Configuration module for Health Tracker Bot
Handles environment variables and settings
"""

import os
from typing import Optional

class Config:
    """Configuration class for bot settings"""
    
    def __init__(self):
        """Initialize configuration from environment variables"""
        
        # Required environment variables
        self.BOT_TOKEN = self._get_required_env("BOT_TOKEN")
        
        # Optional environment variables with defaults
        self.DATABASE_PATH = os.getenv("DATABASE_PATH", "health_tracker.db")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.TIMEZONE = os.getenv("TIMEZONE", "UTC")
        
        # Webhook settings (for production deployment)
        self.WEBHOOK_URL = os.getenv("WEBHOOK_URL")
        self.WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8000"))
        
        # Keep-alive server settings
        self.KEEP_ALIVE_PORT = int(os.getenv("KEEP_ALIVE_PORT", "5000"))
        
        # Health tracking limits and defaults
        self.MAX_WEIGHT_KG = float(os.getenv("MAX_WEIGHT_KG", "500"))
        self.MAX_STEPS = int(os.getenv("MAX_STEPS", "100000"))
        self.MAX_WATER_ML = int(os.getenv("MAX_WATER_ML", "10000"))
        self.MAX_EXERCISE_MINUTES = int(os.getenv("MAX_EXERCISE_MINUTES", "1440"))
        self.MAX_SLEEP_HOURS = float(os.getenv("MAX_SLEEP_HOURS", "24"))
        
        # Daily reminder settings
        self.REMINDER_TIME = os.getenv("REMINDER_TIME", "20:00")  # 8 PM default
        
        self._validate_config()
    
    def _get_required_env(self, key: str) -> str:
        """Get required environment variable or raise error"""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value
    
    def _validate_config(self):
        """Validate configuration values"""
        if len(self.BOT_TOKEN) < 10:
            raise ValueError("BOT_TOKEN appears to be invalid")
        
        if not (1 <= self.KEEP_ALIVE_PORT <= 65535):
            raise ValueError("KEEP_ALIVE_PORT must be between 1 and 65535")
        
        if not (1 <= self.WEBHOOK_PORT <= 65535):
            raise ValueError("WEBHOOK_PORT must be between 1 and 65535")
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return os.getenv("REPLIT_ENVIRONMENT") is not None
    
    def get_database_url(self) -> str:
        """Get database connection URL"""
        return f"sqlite:///{self.DATABASE_PATH}"
