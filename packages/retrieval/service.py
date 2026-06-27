from packages.core.config import Settings
from packages.core.models import DocumentType


class RetrievalService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def search(
        self,
        question: str,
        *,
        product_code: str | None = None,
        doc_type: DocumentType | None = None,
    ) -> list[dict]:
        """Return ranked chunks. Vector/BM25 integration is TODO."""
        _ = (question, product_code, doc_type)
        return []
