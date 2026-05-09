from typing import Optional
from pydantic import BaseModel


class Incident(BaseModel):
    id: str
    system_id: str
    severity: str           # info | warning | critical
    confidence: float       # 0.0–1.0
    started_at: str         # ISO timestamp
    ended_at: str           # ISO timestamp
    duration_minutes: int
    sensors_triggered: list[str]
    anomaly_row_count: int
    suppressed: bool
    suppression_reason: Optional[str] = None
    max_zscores: dict[str, float] = {}
