from fastapi import APIRouter
from pydantic import BaseModel

from app.database.repository import repository

router = APIRouter(prefix="/api/comments", tags=["comments"])

CATEGORIES = {
    "martingale_warning": ["martingale", "double", "recover"],
    "averaging_down_risk": ["average down", "averaging"],
    "news_spike_risk": ["news", "spike", "cpi", "nfp", "fomc"],
    "spread_slippage_risk": ["spread", "slippage"],
    "backtest_forward_gap": ["backtest", "forward"],
    "chop_problem": ["chop", "range", "sideways"],
    "overfitting_risk": ["overfit", "curve"],
    "funded_account_rules": ["funded", "prop", "drawdown"],
    "position_sizing": ["lot", "size", "risk percent"],
    "discord_alerting": ["discord", "alert", "ping"],
}


class CommentIn(BaseModel):
    text: str


def classify_comment(text: str) -> dict:
    lowered = text.lower()
    categories = [name for name, words in CATEGORIES.items() if any(word in lowered for word in words)]
    if any(word in lowered for word in ["martingale", "average down", "slippage", "news", "drawdown"]):
        classification = "KEEP"
    elif any(word in lowered for word in ["maybe", "consider", "could"]):
        classification = "MODIFY"
    elif any(word in lowered for word in ["later", "v2", "future"]):
        classification = "LATER"
    else:
        classification = "IGNORE" if not categories else "MODIFY"
    return {
        "classification": classification,
        "categories": categories or ["general_review"],
        "suggestion": "Stored as review-only learning. It does not directly change trading rules.",
    }


@router.post("")
def add_comment(payload: CommentIn) -> dict:
    result = classify_comment(payload.text)
    comment = repository.add_comment({"text": payload.text, **result})
    return comment.model_dump(mode="json")
