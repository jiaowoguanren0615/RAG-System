from uuid import UUID, uuid4

from fastapi import APIRouter, BackgroundTasks, File, Form, UploadFile

from packages.core.models import DocumentMeta, DocumentStatus, DocumentType

router = APIRouter()

# In-memory store for skeleton
_documents: dict[UUID, DocumentMeta] = {}


@router.get("/documents")
def list_documents(status: DocumentStatus | None = None) -> list[DocumentMeta]:
    docs = list(_documents.values())
    if status:
        docs = [d for d in docs if d.status == status]
    return docs


@router.post("/documents/upload", response_model=DocumentMeta)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    doc_type: DocumentType = Form(DocumentType.SOP),
    title: str | None = Form(None),
) -> DocumentMeta:
    from apps.worker.tasks.indexing import index_document

    meta = DocumentMeta(
        doc_id=uuid4(),
        title=title or (file.filename or "untitled"),
        doc_type=doc_type,
        source_path=file.filename,
    )
    _documents[meta.doc_id] = meta
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    background_tasks.add_task(index_document, str(meta.doc_id), text)
    return meta


@router.post("/documents/{doc_id}/reindex")
def reindex_document(doc_id: UUID) -> dict[str, str]:
    if doc_id not in _documents:
        return {"status": "not_found"}
    return {"status": "queued", "doc_id": str(doc_id)}
