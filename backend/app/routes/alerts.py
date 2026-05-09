from fastapi import APIRouter, HTTPException, Query

from app.models.alert import Alert, AlertFeed
from app.services.pipeline import get_state

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("/", response_model=AlertFeed)
def list_alerts(
    limit: int = Query(default=50, ge=1, le=100, description="Max alerts per category"),
):
    """
    Return active and suppressed alerts.

    Active alerts belong to non-suppressed incidents. Suppressed alerts are
    isolated spikes that did not meet the minimum incident duration threshold —
    surfacing them separately preserves transparency without inflating the
    active alert count.
    """
    state = get_state()
    if not state["ready"]:
        raise HTTPException(status_code=503, detail="Pipeline initializing — try again shortly")

    active = [Alert(**a) for a in state["alerts_active"][:limit]]
    suppressed = [Alert(**a) for a in state["alerts_suppressed"][:limit]]

    return AlertFeed(
        active_alerts=active,
        suppressed_alerts=suppressed,
        total_active=len(state["alerts_active"]),
        total_suppressed=len(state["alerts_suppressed"]),
    )
