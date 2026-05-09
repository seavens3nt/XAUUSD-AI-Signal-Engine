def volatility_state(volatility_score: float, scenario: str) -> dict:
    spike = scenario == "news_spike" or volatility_score >= 82
    return {"spike_detected": spike, "state": "spike" if spike else "normal"}
