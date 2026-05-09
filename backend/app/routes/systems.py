import pandas as pd
from fastapi import APIRouter, HTTPException

from app.models.incident import Incident
from app.models.system import HvacSystemDetail, HvacSystemOverview, SensorReading
from app.services.pipeline import get_state

router = APIRouter(prefix="/systems", tags=["systems"])


@router.get("/", response_model=list[HvacSystemOverview])
def list_systems():
    """
    Return all HVAC systems sorted by operational urgency.

    Systems are ordered: critical → warning → normal, then by ascending health
    score within each severity tier. This ordering directly answers:
    "Where should I go next?"
    """
    state = get_state()
    if not state["ready"]:
        raise HTTPException(status_code=503, detail="Pipeline initializing — try again shortly")
    return [HvacSystemOverview(**s) for s in state["systems"]]


@router.get("/{system_id}", response_model=HvacSystemDetail)
def get_system(system_id: str):
    """
    Return detailed operational data for a specific HVAC system.

    Includes all incidents, the last 20 sensor readings (most recent first),
    and an anomaly rate summary.
    """
    state = get_state()
    if not state["ready"]:
        raise HTTPException(status_code=503, detail="Pipeline initializing — try again shortly")

    system = next((s for s in state["systems"] if s["id"] == system_id), None)
    if system is None:
        raise HTTPException(status_code=404, detail=f"System '{system_id}' not found")

    df: pd.DataFrame = state["anomalies_df"]
    unit_df = (
        df[df["unit_id"] == system_id]
        .sort_values("timestamp", ascending=False)
    )

    # Recent readings (last 20, newest first)
    recent_readings = [
        SensorReading(
            timestamp=row["timestamp"].isoformat(),
            temp=None if pd.isna(row["temp"]) else round(float(row["temp"]), 4),
            pressure=round(float(row["pressure"]), 4),
            airflow=None if pd.isna(row["airflow"]) else round(float(row["airflow"]), 4),
            vibration=round(float(row["vibration"]), 6),
            power=round(float(row["power"]), 4),
            is_imputed=bool(row["is_imputed"]),
            is_anomaly=bool(row["is_anomaly"]),
        )
        for _, row in unit_df.head(20).iterrows()
    ]

    unit_incidents = [i for i in state["incidents"] if i["system_id"] == system_id]
    anomaly_rate = round(float(unit_df["is_anomaly"].mean()), 4)

    return HvacSystemDetail(
        **system,
        anomaly_rate=anomaly_rate,
        incidents=[Incident(**i) for i in unit_incidents],
        recent_readings=recent_readings,
    )
