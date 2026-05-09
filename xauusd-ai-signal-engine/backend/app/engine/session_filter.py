from datetime import datetime, timezone


def session_state(now_iso: str | None = None) -> dict:
    now = datetime.fromisoformat(now_iso.replace("Z", "+00:00")) if now_iso else datetime.now(timezone.utc)
    hour = now.hour
    if 7 <= hour < 16:
        name = "london"
        liquidity = "high"
    elif 13 <= hour < 21:
        name = "new_york"
        liquidity = "high"
    elif 0 <= hour < 6:
        name = "asia"
        liquidity = "medium"
    else:
        name = "rollover"
        liquidity = "thin"
    return {"session": name, "liquidity": liquidity, "is_rollover": name == "rollover"}
