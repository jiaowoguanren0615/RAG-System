from fastapi import FastAPI

from apps.api.routes import audit, chat, documents, feedback
from packages.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Pharma RAG API",
    description="医药企业知识库问答系统",
    version="0.1.0",
    debug=settings.app_debug,
)

app.include_router(chat.router, prefix="/v1", tags=["chat"])
app.include_router(documents.router, prefix="/v1", tags=["documents"])
app.include_router(audit.router, prefix="/v1", tags=["audit"])
app.include_router(feedback.router, prefix="/v1", tags=["feedback"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "env": settings.app_env}


def run() -> None:
    import uvicorn

    uvicorn.run(
        "apps.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.app_debug,
    )
