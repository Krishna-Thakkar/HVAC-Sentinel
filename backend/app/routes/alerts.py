from fastapi import APIRouter

router = APIRouter(prefix="/alerts", tags=["alerts"])


# Phase 1 — implemented in backend foundation phase
@router.get("/")
def list_alerts():
    """Return active and suppressed alerts with incident timeline."""
    return {"message": "Phase 1 — not yet implemented"}
