import numpy as np
import pandas as pd

from app.constants import SENSOR_COLUMNS, Z_SCORE_THRESHOLD, DRIFT_Z_THRESHOLD


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flag anomalous sensor readings using two complementary methods per unit:

    1. Rolling z-score — catches sharp spikes and dips.
       A reading is anomalous if |z-score| > Z_SCORE_THRESHOLD, where z-score
       is computed against the rolling mean/std over the last ROLLING_WINDOW readings.

    2. Rolling mean drift — catches sustained level shifts that rolling z-scores miss
       (rolling stats adapt to gradual changes, masking slow drift).
       A sensor's rolling mean is anomalous if it deviates from the unit's overall
       median by more than DRIFT_Z_THRESHOLD × unit std.

    A row is marked anomalous if either method fires on any sensor.

    Per-unit computation prevents cross-unit contamination and ensures each
    unit is evaluated against its own historical baseline.

    Adds columns:
      {sensor}_zscore         — rolling z-score
      {sensor}_drift_z        — rolling-mean drift z-score vs unit median
      {sensor}_anomaly        — True if either z-score or drift fires
      anomaly_count           — number of sensors flagged in this row
      is_anomaly              — True if any sensor is flagged
      anomalous_sensors       — list of sensor names that triggered
    """
    df = df.copy()
    unit_stats = _compute_unit_stats(df)

    parts = [_detect_unit(group, unit_stats[unit_id]) for unit_id, group in df.groupby("unit_id", sort=True)]
    return pd.concat(parts).reset_index(drop=True)


def _compute_unit_stats(df: pd.DataFrame) -> dict[str, dict[str, tuple[float, float]]]:
    """Pre-compute per-unit median and std for each sensor (used for drift detection)."""
    stats: dict[str, dict[str, tuple[float, float]]] = {}
    for unit_id, group in df.groupby("unit_id"):
        stats[unit_id] = {}
        for col in SENSOR_COLUMNS:
            median = float(group[col].median())
            std = float(group[col].std())
            stats[unit_id][col] = (median, std if std > 1e-10 else np.nan)
    return stats


def _detect_unit(
    group: pd.DataFrame,
    unit_stats: dict[str, tuple[float, float]],
) -> pd.DataFrame:
    group = group.copy()
    flag_cols: list[str] = []

    for col in SENSOR_COLUMNS:
        mean_col = f"{col}_roll_mean"
        std_col = f"{col}_roll_std"
        flag_col = f"{col}_anomaly"

        # --- Method 1: rolling z-score (spike detection) ---
        if mean_col in group.columns and std_col in group.columns:
            valid_std = group[std_col].replace(0.0, np.nan)
            z = (group[col] - group[mean_col]) / valid_std
            group[f"{col}_zscore"] = z.round(3)
            zscore_flag = z.abs().gt(Z_SCORE_THRESHOLD).fillna(False)
        else:
            group[f"{col}_zscore"] = np.nan
            zscore_flag = pd.Series(False, index=group.index)

        # --- Method 2: rolling mean drift (sustained shift detection) ---
        unit_median, unit_std = unit_stats.get(col, (np.nan, np.nan))
        if mean_col in group.columns and not np.isnan(unit_median) and not np.isnan(unit_std):
            drift_z = (group[mean_col] - unit_median) / unit_std
            group[f"{col}_drift_z"] = drift_z.round(3)
            drift_flag = drift_z.abs().gt(DRIFT_Z_THRESHOLD).fillna(False)
        else:
            group[f"{col}_drift_z"] = np.nan
            drift_flag = pd.Series(False, index=group.index)

        # Combined: flag if either method fires
        group[flag_col] = zscore_flag | drift_flag
        flag_cols.append(flag_col)

    group["anomaly_count"] = group[flag_cols].sum(axis=1).astype(int)
    group["is_anomaly"] = group["anomaly_count"] > 0

    group["anomalous_sensors"] = group.apply(
        lambda row: [c.replace("_anomaly", "") for c in flag_cols if row[c]],
        axis=1,
    )

    return group
