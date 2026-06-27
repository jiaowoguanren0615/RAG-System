from packages.core.config import Settings
from packages.core.models import ChatResponse, Citation


class GenerationService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def generate(self, question: str, contexts: list[dict]) -> ChatResponse:
        if not contexts:
            return ChatResponse(
                answer="当前知识库中未找到足够依据，无法回答该问题。",
                citations=[],
                confidence="low",
            )

        citations = [
            Citation(
                doc_id=item["doc_id"],
                title=item["title"],
                version=item.get("version", "v1.0"),
                page=item.get("page"),
                section=item.get("section"),
                snippet=item.get("text", "")[:200],
            )
            for item in contexts[: self.settings.rerank_top_k]
        ]
        return ChatResponse(
            answer=f"（占位回答）基于 {len(citations)} 条参考片段：{question}",
            citations=citations,
            confidence="medium",
        )
