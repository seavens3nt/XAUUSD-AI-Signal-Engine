from __future__ import annotations

from app.database.models import SignalRecord, TraderComment


class InMemoryRepository:
    def __init__(self) -> None:
        self.signals: list[SignalRecord] = []
        self.comments: list[TraderComment] = []

    def add_signal(self, payload: dict) -> SignalRecord:
        record = SignalRecord(id=len(self.signals) + 1, **payload)
        self.signals.insert(0, record)
        return record

    def latest_signal(self) -> SignalRecord | None:
        return self.signals[0] if self.signals else None

    def signal_history(self, limit: int = 25) -> list[SignalRecord]:
        return self.signals[:limit]

    def add_comment(self, payload: dict) -> TraderComment:
        comment = TraderComment(id=len(self.comments) + 1, **payload)
        self.comments.insert(0, comment)
        return comment

    def comment_history(self, limit: int = 25) -> list[TraderComment]:
        return self.comments[:limit]


repository = InMemoryRepository()
