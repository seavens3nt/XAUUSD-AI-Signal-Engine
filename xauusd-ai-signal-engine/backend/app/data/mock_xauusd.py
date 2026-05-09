from __future__ import annotations

import math
import random
from datetime import datetime, timedelta, timezone
from typing import Literal

Scenario = Literal["normal", "choppy", "trending", "news_spike"]


def _candle(ts: datetime, open_price: float, close_price: float, volume: int) -> dict:
    wick = abs(close_price - open_price) * random.uniform(0.45, 1.4) + random.uniform(0.02, 0.18)
    return {
        "time": ts.isoformat(),
        "open": round(open_price, 2),
        "high": round(max(open_price, close_price) + wick, 2),
        "low": round(min(open_price, close_price) - wick, 2),
        "close": round(close_price, 2),
        "tick_volume": volume,
    }


def _series(count: int, step: timedelta, scenario: Scenario, base: float, now: datetime) -> list[dict]:
    candles: list[dict] = []
    price = base
    direction = random.choice([-1, 1])

    for i in range(count):
        ts = now - step * (count - i)
        if scenario == "trending":
            drift = direction * random.uniform(0.45, 1.25)
            noise = random.uniform(-0.2, 0.35)
            volume = random.randint(170, 290)
        elif scenario == "choppy":
            drift = math.sin(i * 1.8) * random.uniform(0.45, 0.95)
            noise = random.uniform(-0.75, 0.75)
            volume = random.randint(80, 160)
        elif scenario == "news_spike":
            drift = random.uniform(-0.35, 0.35)
            if i in {count - 4, count - 3}:
                drift += direction * random.uniform(4.5, 8.5)
            noise = random.uniform(-0.55, 0.55)
            volume = random.randint(260, 520)
        else:
            drift = random.uniform(-0.42, 0.42)
            noise = random.uniform(-0.24, 0.24)
            volume = random.randint(120, 220)

        open_price = price
        close_price = max(1000.0, price + drift + noise)
        candles.append(_candle(ts, open_price, close_price, volume))
        price = close_price
    return candles


def generate_market_snapshot(scenario: Scenario | None = None) -> dict:
    scenario = scenario or random.choices(
        ["normal", "choppy", "trending", "news_spike"],
        weights=[48, 24, 20, 8],
        k=1,
    )[0]
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    base = random.uniform(2285, 2395)

    m1 = _series(15, timedelta(minutes=1), scenario, base, now)
    m5 = _series(15, timedelta(minutes=5), scenario, base - random.uniform(-3, 3), now)
    h1 = _series(15, timedelta(hours=1), scenario, base - random.uniform(-12, 12), now)

    mid = m1[-1]["close"]
    spread_points = {
        "normal": random.uniform(12, 24),
        "choppy": random.uniform(18, 34),
        "trending": random.uniform(14, 28),
        "news_spike": random.uniform(38, 85),
    }[scenario]
    spread = spread_points / 100.0

    return {
        "symbol": "XAUUSD",
        "scenario": scenario,
        "generated_at": now.isoformat(),
        "m1": m1,
        "m5": m5,
        "h1": h1,
        "quote": {
            "bid": round(mid - spread / 2, 2),
            "ask": round(mid + spread / 2, 2),
            "spread": round(spread, 2),
            "spread_points": round(spread_points, 1),
        },
    }
