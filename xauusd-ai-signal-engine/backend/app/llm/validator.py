from __future__ import annotations

from pydantic import ValidationError

from app.config import get_settings
from app.engine.position_sizing import calculate_position_size
from app.llm.schemas import TraderDecision


def validate_trader_decision(raw: dict, context: dict, risk_filters: dict) -> dict:
    settings = get_settings()
    errors: list[str] = []
    try:
        decision = TraderDecision.model_validate(raw)
    except ValidationError as exc:
        return {"status": "REJECTED", "errors": [str(exc)], "decision": None, "position": None}

    if risk_filters["status"] == "BLOCK" and decision.decision != "NO_TRADE":
        errors.append("Hard risk filter says BLOCK")
    if decision.confidence < settings.min_confidence:
        errors.append("Confidence is below minimum")
    if decision.decision in {"BUY", "SELL"}:
        if decision.entry_price is None or decision.stop_loss is None or decision.take_profit is None:
            errors.append("BUY/SELL requires entry, stop_loss, and take_profit")
        elif decision.decision == "BUY" and not (decision.stop_loss < decision.entry_price < decision.take_profit):
            errors.append("BUY SL/TP are on the wrong side")
        elif decision.decision == "SELL" and not (decision.take_profit < decision.entry_price < decision.stop_loss):
            errors.append("SELL SL/TP are on the wrong side")

    position = None
    if not errors and decision.decision in {"BUY", "SELL"}:
        position = calculate_position_size(
            settings.default_account_balance,
            settings.default_risk_percent,
            decision.entry_price,
            decision.stop_loss,
            context["symbol"],
            decision.decision,
            decision.take_profit,
        )
        if position["rr_ratio"] < settings.min_rr:
            errors.append("R:R is below minimum")

    return {
        "status": "REJECTED" if errors else "ACCEPTED",
        "errors": errors,
        "decision": decision.model_dump(),
        "position": position,
    }
