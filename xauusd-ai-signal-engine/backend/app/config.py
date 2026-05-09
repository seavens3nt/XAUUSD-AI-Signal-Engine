from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "XAUUSD AI Signal Engine"
    environment: str = "development"
    discord_webhook_url: str | None = None
    supabase_url: str | None = None
    supabase_service_role_key: str | None = None
    default_account_balance: float = 10000.0
    default_risk_percent: float = 0.5
    max_spread_points: float = 35.0
    min_confidence: float = 0.62
    min_rr: float = 1.5
    daily_loss_limit_percent: float = 3.0
    losing_streak_limit: int = 3

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
