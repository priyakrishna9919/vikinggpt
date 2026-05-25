# =============================================
# Health Check Router
# GET /api/health — used by Railway for uptime
# =============================================

from fastapi import APIRouter
from vectordb.store import get_collection

router = APIRouter()


@router.get("")
async def health():
    """Simple health check — returns DB chunk count."""
    try:
        count = get_collection().count()
        return {"status": "ok", "chunks_in_db": count}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
