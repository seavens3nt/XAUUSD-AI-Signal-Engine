from fastapi import APIRouter, Query

from app.database.repository import repository
from app.scheduler.five_min_loop import run_signal_once

router = APIRouter(prefix="/api/signals", tags=["signals"])


@router.post("/run-once")
async def run_once(scenario: str | None = Query(default=None)) -> dict:
    return await run_signal_once(scenario)


@router.get("/latest")
def latest() -> dict:
    record = repository.latest_signal()
    return record.model_dump(mode="json") if record else {}


@router.get("/history")
def history(limit: int = 25) -> list[dict]:
    return [record.model_dump(mode="json") for record in repository.signal_history(limit)]
