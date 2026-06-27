from apps.worker.celery_app import celery_app
from packages.chunking.strategies import chunk_text
from packages.core.models import DocumentType


@celery_app.task(name="index_document")
def index_document(doc_id: str, content: str, doc_type: str = DocumentType.SOP.value) -> dict:
    """Index a document: chunk text and (TODO) embed + upsert to vector DB."""
    chunks = chunk_text(content, DocumentType(doc_type))
    return {"doc_id": doc_id, "chunk_count": len(chunks), "status": "indexed"}
