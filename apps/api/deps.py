from functools import lru_cache

from packages.core.config import Settings, get_settings
from packages.generation.service import GenerationService
from packages.retrieval.service import RetrievalService


@lru_cache
def get_retrieval_service() -> RetrievalService:
    return RetrievalService(get_settings())


@lru_cache
def get_generation_service() -> GenerationService:
    return GenerationService(get_settings())


def get_app_settings() -> Settings:
    return get_settings()
