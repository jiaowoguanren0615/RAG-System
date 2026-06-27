from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    app_debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    database_url: str = "postgresql+psycopg://rag:rag@localhost:5432/pharma_rag"
    vector_db_url: str = "http://localhost:6333"
    vector_collection: str = "pharma_chunks"

    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "pharma-documents"
    minio_secure: bool = False

    embedding_model: str = "BAAI/bge-m3"
    llm_model: str = "qwen2.5-72b-instruct"
    llm_api_base: str = "http://localhost:8001/v1"
    llm_api_key: str = "changeme"

    default_doc_status_filter: str = "active"
    retrieval_top_k: int = 20
    rerank_top_k: int = 5


@lru_cache
def get_settings() -> Settings:
    return Settings()
