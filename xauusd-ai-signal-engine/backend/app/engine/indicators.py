from __future__ import annotations


def closes(candles: list[dict]) -> list[float]:
    return [float(c["close"]) for c in candles]


def ema(values: list[float], period: int) -> float:
    if not values:
        return 0.0
    alpha = 2 / (period + 1)
    current = values[0]
    for value in values[1:]:
        current = alpha * value + (1 - alpha) * current
    return current


def atr_like(candles: list[dict]) -> float:
    if not candles:
        return 0.0
    ranges = [float(c["high"]) - float(c["low"]) for c in candles]
    return sum(ranges) / len(ranges)


def rsi_like(values: list[float]) -> float:
    if len(values) < 2:
        return 50.0
    gains: list[float] = []
    losses: list[float] = []
    for previous, current in zip(values, values[1:]):
        delta = current - previous
        gains.append(max(delta, 0))
        losses.append(abs(min(delta, 0)))
    avg_gain = sum(gains) / len(gains)
    avg_loss = sum(losses) / len(losses)
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def slope(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return values[-1] - values[0]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))
