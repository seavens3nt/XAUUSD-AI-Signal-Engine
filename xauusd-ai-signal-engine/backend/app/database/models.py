from datetime import datetime, timezone
from pydantic import BaseModel, Field


class SignalRecord(BaseModel):
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    snapshot: dict
    context: dict
    risk_filters: dict
    prompt: str
    llm_decision: dict
    validation: dict
    position: dict | None = None
    alert: dict | None = None


class TraderComment(BaseModel):
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    text: str
    classification: str
    categories: list[str]
    suggestion: str
