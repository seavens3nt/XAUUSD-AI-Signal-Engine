def chop_state(chop_score: float) -> dict:
    if chop_score >= 72:
        state = "too_choppy"
    elif chop_score >= 55:
        state = "mixed"
    else:
        state = "clean"
    return {"state": state, "score": round(chop_score, 2)}
