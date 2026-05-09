from typing import Optional
from pydantic import BaseModel

from app.models.incident import Incident


class SensorReading(BaseModel):
    timestamp: str
    temp: Optional[float] = None
    pressure: float
    airflow: Optional[float] = None
    vibration: float
    power: float
    is_imputed: bool
    is_anomaly: bool


class HvacSystemOverview(BaseModel):
    id: str
    name: str
    health_score: int       # 0–100
    severity: str           # normal | warning | critical
    active_incident_count: int
    suppressed_alert_count: int
    last_updated: str       # ISO timestamp


class HvacSystemDetail(BaseModel):
    id: str
    name: str
    health_score: int
    severity: str
    active_incident_count: int
    suppressed_alert_count: int
    last_updated: str
    anomaly_rate: float             # fraction of rows that were anomalous
    incidents: list[Incident]       # all incidents for this unit
    recent_readings: list[SensorReading]  # last 20 sensor readings
