from fastapi import APIRouter

router = APIRouter(prefix="/systems", tags=["systems"])


# Phase 1 — implemented in backend foundation phase
@router.get("/")
def list_systems():
    """Return overview of all HVAC systems with health scores and incident counts."""
    return {"message": "Phase 1 — not yet implemented"}


@router.get("/{system_id}")
def get_system(system_id: str):
    """Return detailed data for a specific HVAC system."""
    return {"message": "Phase 1 — not yet implemented", "system_id": system_id}
