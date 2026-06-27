# Architecture

See README for the high-level diagram.

## Modules

- `apps/api` — FastAPI HTTP service
- `apps/worker` — Celery indexing tasks
- `packages/ingestion` — document parsing
- `packages/chunking` — doc-type chunking
- `packages/retrieval` — hybrid search
- `packages/generation` — LLM + citations
- `packages/governance` — audit & RBAC (skeleton)
