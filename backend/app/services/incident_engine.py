from typing import Any

import numpy as np
import pandas as pd

from app.constants import (
    CONFIDENCE_MAX_ROWS,
    CONFIDENCE_MIN,
    CRITICAL_DURATION_ROWS,
    CRITICAL_SENSOR_COUNT,
    CRITICAL_SIMULTANEOUS_SENSORS,
    HEALTH_DENSITY_WEIGHT,
    HEALTH_PENALTY_CRITICAL,
    HEALTH_PENALTY_WARNING,
    MIN_INCIDENT_ROWS,
    SENSOR_COLUMNS,
)


def build_incidents(df: pd.DataFrame) -> list[dict[str, Any]]:
    """
    Group consecutive anomalous rows into incidents per unit.

    Separation of concerns:
      - anomaly_detection.py answers: "which rows are anomalous?"
      - This module answers: "do these anomalies constitute an actionable incident?"

    Duration gating:
      Runs with fewer than MIN_INCIDENT_ROWS consecutive anomaly rows are marked
      suppressed — they represent isolated sensor noise, not real incidents.

    Severity rules:
      CRITICAL  → run spans >= CRITICAL_DURATION_ROWS rows, or
                   >= CRITICAL_SENSOR_COUNT sensors triggered simultaneously
      WARNING   → run passes duration gate but does not meet critical thresholds
      INFO      → suppressed (did not pass duration gate)

    Confidence scoring:
      Scales with run duration (more consecutive readings = higher confidence)
      and sensor breadth (more sensors corroborating = higher confidence).
    """
    all_incidents: list[dict[str, Any]] = []

    for unit_id in sorted(df["unit_id"].unique()):
        unit_df = df[df["unit_id"] == unit_id].copy().reset_index(drop=True)
        unit_incidents = _build_unit_incidents(unit_df, unit_id)
        all_incidents.extend(unit_incidents)

    return all_incidents


def compute_system_health(
    incidents: list[dict[str, Any]],
    total_rows: int,
    anomaly_rows: int,
) -> tuple[int, str]:
    """
    Derive health score (0–100) and severity label for a single unit.

    Two additive penalty components:
      1. Anomaly density: fraction of rows that were anomalous × HEALTH_DENSITY_WEIGHT
      2. Incident severity: fixed penalty per active (non-suppressed) incident

    Returns (health_score, severity_label).
    """
    active = [i for i in incidents if not i["suppressed"]]

    density = anomaly_rows / total_rows if total_rows > 0 else 0.0
    density_penalty = density * HEALTH_DENSITY_WEIGHT

    severity_penalty = 0
    for inc in active:
        if inc["severity"] == "critical":
            severity_penalty += HEALTH_PENALTY_CRITICAL
        elif inc["severity"] == "warning":
            severity_penalty += HEALTH_PENALTY_WARNING

    health_score = max(0, round(100.0 - min(100.0, density_penalty + severity_penalty)))

    severities = {i["severity"] for i in active}
    if "critical" in severities:
        label = "critical"
    elif "warning" in severities:
        label = "warning"
    else:
        label = "normal"

    return health_score, label


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _build_unit_incidents(
    unit_df: pd.DataFrame,
    unit_id: str,
) -> list[dict[str, Any]]:
    incidents: list[dict[str, Any]] = []

    # Identify consecutive anomaly runs.
    # Each time is_anomaly flips False→True or stays True, the cumsum of (~is_anomaly)
    # stays constant, grouping the True block into a single run_id.
    unit_df = unit_df.copy()
    unit_df["_run_id"] = (~unit_df["is_anomaly"]).cumsum()

    anomaly_rows = unit_df[unit_df["is_anomaly"]]
    if anomaly_rows.empty:
        return incidents

    for _run_id, run in anomaly_rows.groupby("_run_id"):
        n_rows = len(run)

        # Collect sensors before suppression decision — needed for multi-sensor check
        all_triggered_pre: set[str] = set()
        for sensors in run["anomalous_sensors"]:
            if isinstance(sensors, list):
                all_triggered_pre.update(sensors)
        n_sensors_pre = len(all_triggered_pre)

        # Duration gating with multi-sensor exception:
        # A single-row run is NOT suppressed if it involves >= CRITICAL_SENSOR_COUNT
        # simultaneous sensor anomalies. Correlated multi-sensor events indicate a
        # real operational problem even if they resolve quickly.
        suppressed = n_rows < MIN_INCIDENT_ROWS and n_sensors_pre < CRITICAL_SENSOR_COUNT

        # Collect all sensors triggered across any row in this run
        all_triggered: set[str] = set()
        for sensors in run["anomalous_sensors"]:
            if isinstance(sensors, list):
                all_triggered.update(sensors)
        sensors_triggered = sorted(all_triggered)
        n_sensors = len(sensors_triggered)

        # Severity determination:
        #   CRITICAL if: 3+ sensors simultaneously (acute multi-failure signal)
        #             OR 4+ consecutive anomaly rows (sustained anomaly)
        #             OR 2+ sensors AND 2+ rows (corroborated + sustained)
        #   WARNING  if: passed suppression gate but does not meet critical thresholds
        #   INFO     if: suppressed (isolated noise)
        if suppressed:
            severity = "info"
        elif (
            n_sensors >= CRITICAL_SIMULTANEOUS_SENSORS
            or n_rows >= CRITICAL_DURATION_ROWS
            or (n_sensors >= CRITICAL_SENSOR_COUNT and n_rows >= MIN_INCIDENT_ROWS)
        ):
            severity = "critical"
        else:
            severity = "warning"

        # Confidence
        if suppressed:
            confidence = 0.0
        else:
            duration_factor = min(1.0, n_rows / CONFIDENCE_MAX_ROWS)
            sensor_factor = min(1.0, n_sensors / len(SENSOR_COLUMNS))
            raw = 0.5 * duration_factor + 0.5 * (0.4 + 0.6 * sensor_factor)
            confidence = round(max(CONFIDENCE_MIN, raw), 2)

        start_ts = run["timestamp"].iloc[0]
        end_ts = run["timestamp"].iloc[-1]
        # Each row spans 5 minutes; add one interval to include the final reading's window
        duration_minutes = max(5, int((end_ts - start_ts).total_seconds() / 60) + 5)

        incidents.append({
            "id": f"{unit_id}_INC_{len(incidents):03d}",
            "system_id": unit_id,
            "severity": severity,
            "confidence": confidence,
            "started_at": start_ts.isoformat(),
            "ended_at": end_ts.isoformat(),
            "duration_minutes": duration_minutes,
            "sensors_triggered": sensors_triggered,
            "anomaly_row_count": n_rows,
            "suppressed": suppressed,
            "suppression_reason": (
                "Isolated spike — single reading below minimum incident duration"
                if suppressed
                else None
            ),
            "max_zscores": _peak_zscores(run, sensors_triggered),
        })

    return incidents


def _peak_zscores(rows: pd.DataFrame, sensors: list[str]) -> dict[str, float]:
    """Return the peak absolute z-score per sensor for operational context."""
    result: dict[str, float] = {}
    for sensor in sensors:
        z_col = f"{sensor}_zscore"
        if z_col in rows.columns:
            peak = rows[z_col].abs().max()
            result[sensor] = round(float(peak), 2) if not np.isnan(peak) else 0.0
    return result
