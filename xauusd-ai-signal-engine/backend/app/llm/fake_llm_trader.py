from __future__ import annotations


def get_fake_llm_decision(context: dict, risk_filters: dict) -> dict:
    if risk_filters["status"] == "BLOCK":
        return {
            "decision": "NO_TRADE",
            "confidence": 0.9,
            "entry_price": None,
            "stop_loss": None,
            "take_profit": None,
            "order_type": "NONE",
            "thesis": "Hard filters block new paper signals.",
            "reason_codes": risk_filters["blocked_by"],
            "invalidate_if": [],
        }

    quote = context["quote"]
    mid = round((quote["bid"] + quote["ask"]) / 2, 2)
    trend = context["trend"]["direction"]
    if context["scenario"] == "trending" and trend == "neutral":
        trend = "bullish" if context["trend"]["m5_slope"] >= 0 else "bearish"
    momentum = context["momentum"]["score"]
    volatility = max(context["volatility"]["score"], 12)
    stop_distance = round(max(1.6, volatility / 14), 2)
    target_distance = round(stop_distance * 1.8, 2)

    max_trade_chop = 72 if context["scenario"] == "trending" else 62

    if trend == "bullish" and momentum < 74 and context["chop"]["score"] < max_trade_chop:
        return {
            "decision": "BUY",
            "confidence": 0.68,
            "entry_price": quote["ask"],
            "stop_loss": round(mid - stop_distance, 2),
            "take_profit": round(mid + target_distance, 2),
            "order_type": "BUY_MARKET",
            "thesis": "Bullish trend with acceptable momentum and manageable chop.",
            "reason_codes": ["trend_bullish", "momentum_ok", "risk_filters_pass"],
            "invalidate_if": ["M1 closes below stop structure", "spread widens above limit"],
        }
    if trend == "bearish" and momentum > 26 and context["chop"]["score"] < max_trade_chop:
        return {
            "decision": "SELL",
            "confidence": 0.68,
            "entry_price": quote["bid"],
            "stop_loss": round(mid + stop_distance, 2),
            "take_profit": round(mid - target_distance, 2),
            "order_type": "SELL_MARKET",
            "thesis": "Bearish trend with acceptable momentum and manageable chop.",
            "reason_codes": ["trend_bearish", "momentum_ok", "risk_filters_pass"],
            "invalidate_if": ["M1 closes above stop structure", "spread widens above limit"],
        }
    return {
        "decision": "NO_TRADE",
        "confidence": 0.74,
        "entry_price": None,
        "stop_loss": None,
        "take_profit": None,
        "order_type": "NONE",
        "thesis": "No clean directional edge in the current mock context.",
        "reason_codes": ["no_clear_edge"],
        "invalidate_if": [],
    }
