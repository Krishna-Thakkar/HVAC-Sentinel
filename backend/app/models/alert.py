from typing import Optional
from pydantic import BaseModel


class Alert(BaseModel):
    id: str
    system_id: str
    sensor: str
    value: float
    z_score: float
    timestamp: str          # ISO timestamp
    incident_id: Optional[str] = None
    suppressed: bool
    suppression_reason: Optional[str] = None


class AlertFeed(BaseModel):
    active_alerts: list[Alert]
    suppressed_alerts: list[Alert]
    total_active: int
    total_suppressed: int
