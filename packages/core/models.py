from datetime import date
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DocumentType(StrEnum):
    LABEL = "label"
    SOP = "sop"
    REGULATION = "regulation"
    CLINICAL = "clinical"
    PV = "pv"
    SPEC = "spec"


class DocumentStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class DocumentMeta(BaseModel):
    doc_id: UUID = Field(default_factory=uuid4)
    title: str
    doc_type: DocumentType
    department: str | None = None
    product_code: str | None = None
    version: str = "v1.0"
    effective_date: date | None = None
    status: DocumentStatus = DocumentStatus.ACTIVE
    classification: str = "internal"
    source_path: str | None = None
    checksum: str | None = None


class Citation(BaseModel):
    doc_id: UUID
    title: str
    version: str
    page: int | None = None
    section: str | None = None
    snippet: str


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    stream: bool = False
    product_code: str | None = None
    doc_type: DocumentType | None = None


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    confidence: str = "low"
    disclaimer: str = (
        "以上内容仅供内部查阅，不构成注册、临床或用药建议。请以最新批准文件为准。"
    )


class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int = Field(ge=1, le=5)
    comment: str | None = None
