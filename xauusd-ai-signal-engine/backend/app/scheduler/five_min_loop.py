from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.alerts.discord import maybe_send_discord_alert
from app.data.mock_xauusd import generate_market_snapshot
from app.database.repository import repository
from app.engine.market_context import compute_market_context
from app.engine.prompt_builder import build_trader_prompt
from app.engine.risk_guard import evaluate_hard_filters
from app.llm.fake_llm_trader import get_fake_llm_decision
from app.llm.validator import validate_trader_decision


async def run_signal_once(scenario: str | None = None) -> dict:
    snapshot = generate_market_snapshot(scenario)
    context = compute_market_context(snapshot)
    risk_filters = evaluate_hard_filters(context)
    prompt = build_trader_prompt(context, risk_filters)
    llm_decision = get_fake_llm_decision(context, risk_filters)
    validation = validate_trader_decision(llm_decision, context, risk_filters)
    payload = {
        "snapshot": snapshot,
        "context": context,
        "risk_filters": risk_filters,
        "prompt": prompt,
        "llm_decision": validation["decision"] or llm_decision,
        "validation": validation,
        "position": validation["position"],
        "alert": None,
    }
    record = repository.add_signal(payload).model_dump(mode="json")
    if record["llm_decision"]["decision"] != "NO_TRADE" or record["risk_filters"]["status"] == "BLOCK":
        record["alert"] = await maybe_send_discord_alert(record)
    return record


def create_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_signal_once, "interval", minutes=5, id="five_min_signal_loop", max_instances=1)
    return scheduler
