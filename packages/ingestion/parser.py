from pathlib import Path

from packages.core.models import DocumentMeta, DocumentType


def parse_document(path: Path, doc_type: DocumentType, title: str | None = None) -> DocumentMeta:
    """Parse a document file and return metadata. Content extraction is TODO."""
    return DocumentMeta(
        title=title or path.stem,
        doc_type=doc_type,
        source_path=str(path),
        checksum=None,
    )
