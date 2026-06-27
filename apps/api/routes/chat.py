from fastapi import APIRouter, Depends

from apps.api.deps import get_generation_service, get_retrieval_service
from packages.core.models import ChatRequest, ChatResponse
from packages.generation.service import GenerationService
from packages.governance.audit import AuditLogger
from packages.retrieval.service import RetrievalService

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    retrieval: RetrievalService = Depends(get_retrieval_service),
    generation: GenerationService = Depends(get_generation_service),
) -> ChatResponse:
    contexts = retrieval.search(
        payload.question,
        product_code=payload.product_code,
        doc_type=payload.doc_type,
    )
    response = generation.generate(payload.question, contexts)
    AuditLogger.log_chat(
        user_id="anonymous",
        question=payload.question,
        answer=response.answer,
        citations=[c.model_dump(mode="json") for c in response.citations],
    )
    return response
