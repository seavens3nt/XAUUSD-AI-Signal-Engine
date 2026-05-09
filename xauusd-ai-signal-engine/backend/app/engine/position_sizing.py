from __future__ import annotations


def calculate_position_size(
    account_balance: float,
    risk_percent: float,
    entry_price: float,
    stop_loss: float,
    symbol: str,
    direction: str,
    take_profit: float | None = None,
) -> dict:
    dollar_risk = account_balance * (risk_percent / 100)
    stop_distance = abs(entry_price - stop_loss)
    if stop_distance <= 0:
        return {"suggested_lot_size": 0.0, "dollar_risk": 0.0, "risk_percent": risk_percent, "reward_estimate": 0.0, "rr_ratio": 0.0}

    # Placeholder XAUUSD model: 1.00 lot is treated as 100 oz; real broker specs arrive in V2.
    suggested_lot_size = dollar_risk / (stop_distance * 100)
    reward_estimate = abs((take_profit or entry_price) - entry_price) * suggested_lot_size * 100
    rr_ratio = reward_estimate / dollar_risk if dollar_risk else 0
    return {
        "symbol": symbol,
        "direction": direction,
        "suggested_lot_size": round(max(suggested_lot_size, 0), 2),
        "dollar_risk": round(dollar_risk, 2),
        "risk_percent": risk_percent,
        "reward_estimate": round(reward_estimate, 2),
        "rr_ratio": round(rr_ratio, 2),
    }
