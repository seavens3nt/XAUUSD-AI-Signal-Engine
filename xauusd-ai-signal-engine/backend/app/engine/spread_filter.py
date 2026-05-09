def spread_state(spread_points: float, max_spread_points: float) -> dict:
    if spread_points > max_spread_points:
        state = "blocked"
    elif spread_points > max_spread_points * 0.75:
        state = "elevated"
    else:
        state = "normal"
    return {"state": state, "spread_points": spread_points, "max_spread_points": max_spread_points}
