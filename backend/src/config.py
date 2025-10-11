from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """Application settings with environment-based configuration."""

    # Application
    app_name: str = "TaskFlow API"
    environment: str = "development"
    debug: bool = True

    # Database
    mongodb_url: str = "mongodb://localhost:27017"

    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # Monitoring (optional)
    sentry_dsn: str = ""

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
