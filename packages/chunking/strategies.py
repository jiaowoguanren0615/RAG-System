from packages.core.models import DocumentType


def chunk_text(text: str, doc_type: DocumentType, chunk_size: int = 800) -> list[dict]:
    """Split text into chunks with section metadata. Placeholder implementation."""
    if not text.strip():
        return []

    chunks: list[dict] = []
    start = 0
    index = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(
            {
                "index": index,
                "text": text[start:end],
                "section": f"chunk-{index + 1}",
                "doc_type": doc_type.value,
            }
        )
        start = end
        index += 1
    return chunks
