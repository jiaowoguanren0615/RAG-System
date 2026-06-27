from fastapi import APIRouter

from packages.core.models import FeedbackRequest

router = APIRouter()

_feedback_store: list[FeedbackRequest] = []


@router.post("/feedback")
def submit_feedback(payload: FeedbackRequest) -> dict[str, str]:
    _feedback_store.append(payload)
    return {"status": "received"}
