import json


def build_trader_prompt(context: dict, risk_filters: dict) -> str:
    payload = {
        "mode": "PAPER_ASSISTED_ONLY",
        "instruction": "Return strict JSON only. Do not suggest martingale, averaging down, or live execution.",
        "market_context": context,
        "hard_filters": risk_filters,
        "schema": {
            "decision": "NO_TRADE | BUY | SELL",
            "confidence": "0.0-1.0",
            "entry_price": "number|null",
            "stop_loss": "number|null",
            "take_profit": "number|null",
            "order_type": "NONE | BUY_MARKET | SELL_MARKET",
            "thesis": "short string",
            "reason_codes": ["strings"],
            "invalidate_if": ["strings"],
        },
    }
    return json.dumps(payload, indent=2)
