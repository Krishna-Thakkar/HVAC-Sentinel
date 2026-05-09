import numpy as np
import pandas as pd

from app.constants import SENSOR_COLUMNS, ROLLING_WINDOW, MIN_ROLLING_PERIODS


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Generate rolling statistics and derived operational features per unit."""
    df = df.copy()

    parts = [_engineer_unit(group) for _, group in df.groupby("unit_id", sort=True)]
    return pd.concat(parts).reset_index(drop=True)


def _engineer_unit(group: pd.DataFrame) -> pd.DataFrame:
    group = group.copy()

    for col in SENSOR_COLUMNS:
        roll = group[col].rolling(ROLLING_WINDOW, min_periods=MIN_ROLLING_PERIODS)
        # Baseline statistics used by anomaly detection for z-score computation
        group[f"{col}_roll_mean"] = roll.mean()
        group[f"{col}_roll_std"] = roll.std()
        # Rate of change per minute; readings are 5-minute intervals
        group[f"{col}_roc"] = group[col].diff() / 5.0

    # Vibration delta: absolute change between readings highlights sudden mechanical events
    group["vibration_delta"] = group["vibration"].diff().abs()

    # Airflow-pressure ratio: sustained deviation suggests duct obstruction or fan degradation
    safe_pressure = group["pressure"].replace(0, np.nan)
    group["ap_ratio"] = group["airflow"] / safe_pressure
    group["ap_ratio_roll_mean"] = (
        group["ap_ratio"]
        .rolling(ROLLING_WINDOW, min_periods=MIN_ROLLING_PERIODS)
        .mean()
    )
    group["ap_ratio_deviation"] = (group["ap_ratio"] - group["ap_ratio_roll_mean"]).abs()

    # Trend: rolling mean of rate-of-change reveals sustained directional movement
    for col in ["temp", "vibration", "airflow"]:
        group[f"{col}_trend"] = (
            group[f"{col}_roc"]
            .rolling(ROLLING_WINDOW, min_periods=MIN_ROLLING_PERIODS)
            .mean()
        )

    return group
