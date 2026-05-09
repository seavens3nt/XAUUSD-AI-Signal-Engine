from typing import Literal
from pydantic import BaseModel, Field


Decision = Literal["NO_TRADE", "BUY", "SELL"]
OrderType = Literal["NONE", "BUY_MARKET", "SELL_MARKET"]


class TraderDecision(BaseModel):
    decision: Decision
    confidence: float = Field(ge=0.0, le=1.0)
    entry_price: float | None = None
    stop_loss: float | None = None
    take_profit: float | None = None
    order_type: OrderType
    thesis: str
    reason_codes: list[str] = []
    invalidate_if: list[str] = []
