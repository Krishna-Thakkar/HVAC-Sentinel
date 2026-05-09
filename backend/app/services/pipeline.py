"""
Pipeline orchestrator for HVAC Sentinel.

Runs the full data processing chain once at server startup and caches
all results in a module-level dictionary. API routes read from this cache
rather than recomputing on every request.

This design is appropriate for a dataset-based prototype — no database or
streaming infrastructure required. The pipeline is deterministic and
reproducible on every restart.
"""
from typing import Any

import pandas as pd

from app.services.data_loader import load_raw_data, save_processed
from app.services.preprocessing import preprocess
from app.services.feature_engineering import engineer_features
from app.services.anomaly_detection import detect_anomalies
from app.services.incident_engine import build_incidents, compute_system_health

# ---------------------------------------------------------------------------
# In-memory state — populated once during the startup lifespan event
# ---------------------------------------------------------------------------

_state: dict[str, Any] = {
    "ready": False,
    "systems": [],          # List[dict] — HvacSystemOverview shape
    "incidents": [],        # List[dict] — all incidents, all units
    "alerts_active": [],    # List[dict] — active alert rows (non-suppressed incidents)
    "alerts_suppressed": [], # List[dict] — suppressed alert rows
    "anomalies_df": None,   # Full anomaly-tagged DataFrame for detail views
}


def run_pipeline() -> None:
    """Execute the full HVAC Sentinel data pipeline and populate the cache."""
    print("[Pipeline] Loading raw dataset...")
    raw_df = load_raw_data()

    print("[Pipeline] Preprocessing...")
    processed_df = preprocess(raw_df)
    save_processed(processed_df, "01_preprocessed")

    print("[Pipeline] Engineering features...")
    features_df = engineer_features(processed_df)
    save_processed(features_df, "02_features")

    print("[Pipeline] Detecting anomalies...")
    anomalies_df = detect_anomalies(features_df)
    save_processed(anomalies_df, "03_anomalies")

    print("[Pipeline] Building incidents...")
    all_incidents = build_incidents(anomalies_df)

    systems = _build_system_overviews(anomalies_df, all_incidents)
    active_alerts, suppressed_alerts = _build_alert_feed(anomalies_df, all_incidents)

    _state.update({
        "ready": True,
        "systems": systems,
        "incidents": all_incidents,
        "alerts_active": active_alerts,
        "alerts_suppressed": suppressed_alerts,
        "anomalies_df": anomalies_df,
    })

    active_inc = sum(1 for i in all_incidents if not i["suppressed"])
    suppressed_inc = len(all_incidents) - active_inc
    print(
        f"[Pipeline] Complete — {len(systems)} systems | "
        f"{active_inc} active incidents | {suppressed_inc} suppressed | "
        f"{len(active_alerts)} active alerts"
    )


def get_state() -> dict[str, Any]:
    return _state


# ---------------------------------------------------------------------------
# Private builders — transform pipeline outputs into API-ready structures
# ---------------------------------------------------------------------------

def _build_system_overviews(
    df: pd.DataFrame,
    incidents: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    systems: list[dict[str, Any]] = []

    for unit_id in sorted(df["unit_id"].unique()):
        unit_df = df[df["unit_id"] == unit_id]
        unit_incidents = [i for i in incidents if i["system_id"] == unit_id]

        total_rows = len(unit_df)
        anomaly_rows = int(unit_df["is_anomaly"].sum())

        health_score, severity = compute_system_health(unit_incidents, total_rows, anomaly_rows)

        active_inc = [i for i in unit_incidents if not i["suppressed"]]
        suppressed_inc = [i for i in unit_incidents if i["suppressed"]]

        systems.append({
            "id": unit_id,
            "name": f"HVAC Unit {unit_id.split('_')[1]}",
            "health_score": health_score,
            "severity": severity,
            "active_incident_count": len(active_inc),
            "suppressed_alert_count": len(suppressed_inc),
            "last_updated": unit_df["timestamp"].max().isoformat(),
        })

    # Sort by urgency: critical first, then warning, then by ascending health score
    _severity_rank = {"critical": 0, "warning": 1, "normal": 2}
    systems.sort(key=lambda s: (_severity_rank.get(s["severity"], 3), s["health_score"]))
    return systems


def _build_alert_feed(
    df: pd.DataFrame,
    incidents: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Build individual sensor-level alert rows from anomaly-tagged data.

    Each anomalous row can produce one alert per flagged sensor, giving
    technicians granular visibility into which specific sensor triggered.
    """
    active: list[dict[str, Any]] = []
    suppressed: list[dict[str, Any]] = []

    anomaly_rows = df[df["is_anomaly"]].copy()

    for _, row in anomaly_rows.iterrows():
        unit_id = str(row["unit_id"])
        parent = _find_parent_incident(incidents, unit_id, row["timestamp"])

        sensors = row["anomalous_sensors"]
        if not isinstance(sensors, list):
            continue

        for sensor in sensors:
            z_col = f"{sensor}_zscore"
            drift_col = f"{sensor}_drift_z"
            roll_z = float(row[z_col]) if z_col in row.index and not pd.isna(row[z_col]) else 0.0
            drift_z = float(row[drift_col]) if drift_col in row.index and not pd.isna(row[drift_col]) else 0.0
            # Report whichever method produced the stronger signal
            z_score = roll_z if abs(roll_z) >= abs(drift_z) else drift_z

            alert = {
                "id": f"{unit_id}_ALERT_{row['timestamp'].strftime('%H%M')}_{sensor}",
                "system_id": unit_id,
                "sensor": sensor,
                "value": round(float(row[sensor]), 4) if not pd.isna(row[sensor]) else 0.0,
                "z_score": round(z_score, 2),
                "timestamp": row["timestamp"].isoformat(),
                "incident_id": parent["id"] if parent else None,
                "suppressed": parent["suppressed"] if parent else True,
                "suppression_reason": (
                    parent.get("suppression_reason")
                    if parent and parent["suppressed"]
                    else None
                ),
            }

            if alert["suppressed"]:
                suppressed.append(alert)
            else:
                active.append(alert)

    active.sort(key=lambda a: a["timestamp"], reverse=True)
    suppressed.sort(key=lambda a: a["timestamp"], reverse=True)

    # Cap response size — prevents unbounded payload on larger datasets
    return active[:100], suppressed[:100]


def _find_parent_incident(
    incidents: list[dict[str, Any]],
    unit_id: str,
    timestamp: pd.Timestamp,
) -> dict[str, Any] | None:
    """Return the incident whose time window contains this timestamp, or None."""
    for inc in incidents:
        if inc["system_id"] != unit_id:
            continue
        if pd.Timestamp(inc["started_at"]) <= timestamp <= pd.Timestamp(inc["ended_at"]):
            return inc
    return None
