from fastapi import APIRouter

from packages.governance.audit import AuditLogger

router = APIRouter()


@router.get("/audit/logs")
def list_audit_logs(limit: int = 50) -> list[dict]:
    return AuditLogger.list_logs(limit=limit)
