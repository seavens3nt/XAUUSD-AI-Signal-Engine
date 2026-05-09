def news_state(scenario: str) -> dict:
    active = scenario == "news_spike"
    return {
        "blackout_active": active,
        "severity": "high" if active else "low",
        "reason": "Mock news-spike scenario" if active else "No scheduled mock blackout",
    }
