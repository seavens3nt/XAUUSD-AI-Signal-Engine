from __future__ import annotations

from app.config import get_settings
from app.engine.chop_filter import chop_state
from app.engine.indicators import atr_like, clamp, closes, ema, rsi_like, slope
from app.engine.news_filter import news_state
from app.engine.session_filter import session_state
from app.engine.spread_filter import spread_state
from app.engine.volatility_guard import volatility_state


def compute_market_context(snapshot: dict) -> dict:
    settings = get_settings()
    m1 = snapshot["m1"]
    m5 = snapshot["m5"]
    h1 = snapshot["h1"]
    m1_closes = closes(m1)
    m5_closes = closes(m5)
    h1_closes = closes(h1)

    fast = ema(m5_closes, 5)
    slow = ema(m5_closes, 12)
    h1_fast = ema(h1_closes, 5)
    h1_slow = ema(h1_closes, 12)
    trend_raw = ((fast - slow) + (h1_fast - h1_slow)) * 10
    trend_score = clamp(50 + trend_raw, 0, 100)

    momentum = rsi_like(m1_closes)
    atr_m1 = atr_like(m1)
    volatility_score = clamp(atr_m1 * 16, 0, 100)
    if snapshot["scenario"] == "news_spike":
        volatility_score = max(volatility_score, 90)

    latest = m1_closes[-1]
    ema_anchor = ema(m5_closes, 8)
    distance = latest - ema_anchor
    mean_reversion_pressure = clamp(abs(distance) * 14, 0, 100)
    direction_changes = sum(
        1
        for a, b, c in zip(m1_closes, m1_closes[1:], m1_closes[2:])
        if (b - a) * (c - b) < 0
    )
    chop_score = clamp(direction_changes / max(len(m1_closes) - 2, 1) * 100, 0, 100)
    if snapshot["scenario"] == "choppy":
        chop_score = max(chop_score, 76)
    volume_avg = sum(c["tick_volume"] for c in m1) / len(m1)
    volume_state = "high" if volume_avg > 240 else "low" if volume_avg < 110 else "normal"

    quote = snapshot["quote"]
    spread = spread_state(quote["spread_points"], settings.max_spread_points)
    news = news_state(snapshot["scenario"])
    volatility = volatility_state(volatility_score, snapshot["scenario"])
    chop = chop_state(chop_score)

    direction = "bullish" if trend_score >= 53 else "bearish" if trend_score <= 47 else "neutral"
    return {
        "symbol": snapshot["symbol"],
        "scenario": snapshot["scenario"],
        "generated_at": snapshot["generated_at"],
        "quote": quote,
        "trend": {"direction": direction, "score": round(trend_score, 2), "m5_slope": round(slope(m5_closes), 2)},
        "momentum": {"score": round(momentum, 2), "state": "overbought" if momentum > 70 else "oversold" if momentum < 30 else "balanced"},
        "mean_reversion": {"pressure": round(mean_reversion_pressure, 2), "ema_distance": round(distance, 2)},
        "vwap_ema_distance_estimate": round(distance, 2),
        "volatility": {"score": round(volatility_score, 2), **volatility},
        "chop": chop,
        "volume": {"state": volume_state, "average_tick_volume": round(volume_avg, 2)},
        "spread": spread,
        "session": session_state(snapshot["generated_at"]),
        "news": news,
    }
