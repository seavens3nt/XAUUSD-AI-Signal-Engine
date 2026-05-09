from __future__ import annotations

from app.config import get_settings


def evaluate_hard_filters(context: dict, risk_memory: dict | None = None) -> dict:
    settings = get_settings()
    risk_memory = risk_memory or {"daily_loss_percent": 0.0, "losing_streak": 0, "open_position": None}
    checks = {
        "no_martingale": {"status": "PASS", "reason": "Lot escalation after losses is disabled in V1"},
        "no_averaging_down": {"status": "PASS", "reason": "Multiple entries against a losing trade are disabled"},
        "no_adding_to_losers": {"status": "PASS", "reason": "Open losing-position adds are blocked"},
        "spread": {"status": "PASS", "reason": "Spread acceptable"},
        "volatility_spike": {"status": "PASS", "reason": "No volatility spike"},
        "chop": {"status": "PASS", "reason": "Chop acceptable"},
        "news_blackout": {"status": "PASS", "reason": "No news blackout"},
        "daily_loss_limit": {"status": "PASS", "reason": "Daily loss under limit"},
        "losing_streak_limit": {"status": "PASS", "reason": "Losing streak under limit"},
    }

    if context["spread"]["state"] == "blocked":
        checks["spread"] = {"status": "BLOCK", "reason": "Spread exceeds configured maximum"}
    if context["volatility"]["spike_detected"]:
        checks["volatility_spike"] = {"status": "BLOCK", "reason": "Volatility spike detected"}
    if context["chop"]["state"] == "too_choppy":
        checks["chop"] = {"status": "BLOCK", "reason": "Market is too choppy"}
    if context["news"]["blackout_active"]:
        checks["news_blackout"] = {"status": "BLOCK", "reason": context["news"]["reason"]}
    if risk_memory.get("daily_loss_percent", 0) >= settings.daily_loss_limit_percent:
        checks["daily_loss_limit"] = {"status": "BLOCK", "reason": "Daily loss limit reached"}
    if risk_memory.get("losing_streak", 0) >= settings.losing_streak_limit:
        checks["losing_streak_limit"] = {"status": "BLOCK", "reason": "Losing streak limit reached"}

    blocked = [name for name, check in checks.items() if check["status"] == "BLOCK"]
    return {"status": "BLOCK" if blocked else "PASS", "blocked_by": blocked, "checks": checks, "risk_memory": risk_memory}
