from __future__ import annotations

import httpx

from app.config import get_settings


def format_discord_alert(record: dict) -> str:
    decision = record["llm_decision"]["decision"]
    position = record.get("position") or {}
    validation = record["validation"]
    return "\n".join(
        [
            f"**XAUUSD Paper Signal:** {decision}",
            f"Order: {record['llm_decision']['order_type']}",
            f"Entry: {record['llm_decision']['entry_price']} | SL: {record['llm_decision']['stop_loss']} | TP: {record['llm_decision']['take_profit']}",
            f"Lot: {position.get('suggested_lot_size')} | Risk: ${position.get('dollar_risk')} | Reward: ${position.get('reward_estimate')} | R:R: {position.get('rr_ratio')}",
            f"Confidence: {record['llm_decision']['confidence']}",
            f"Filters: {record['risk_filters']['status']} {record['risk_filters']['blocked_by']}",
            f"Validation: {validation['status']} {validation['errors']}",
            f"Reason: {record['llm_decision']['thesis']}",
            "_Mode: PAPER / ASSISTED DECISION ONLY. No broker execution._",
        ]
    )


async def maybe_send_discord_alert(record: dict) -> dict:
    settings = get_settings()
    message = format_discord_alert(record)
    if not settings.discord_webhook_url:
        return {"sent": False, "reason": "DISCORD_WEBHOOK_URL is not set", "message": message}
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(settings.discord_webhook_url, json={"content": message})
    return {"sent": response.is_success, "status_code": response.status_code, "message": message}
