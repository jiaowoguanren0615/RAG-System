from datetime import UTC, datetime
from uuid import uuid4


class AuditLogger:
    """In-memory audit logger for skeleton. Replace with DB persistence."""

    _records: list[dict] = []

    @classmethod
    def log_chat(cls, *, user_id: str, question: str, answer: str, citations: list) -> dict:
        record = {
            "id": str(uuid4()),
            "user_id": user_id,
            "question": question,
            "answer": answer,
            "citations": citations,
            "created_at": datetime.now(UTC).isoformat(),
        }
        cls._records.append(record)
        return record

    @classmethod
    def list_logs(cls, limit: int = 50) -> list[dict]:
        return list(reversed(cls._records[-limit:]))
