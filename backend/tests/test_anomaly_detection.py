import pandas as pd
from app.constants import SENSOR_COLUMNS


def test_is_anomaly_column_exists(anomalies_df):
    assert "is_anomaly" in anomalies_df.columns


def test_anomaly_count_column_exists(anomalies_df):
    assert "anomaly_count" in anomalies_df.columns


def test_anomalous_sensors_column_exists(anomalies_df):
    assert "anomalous_sensors" in anomalies_df.columns


def test_zscore_columns_created(anomalies_df):
    for col in SENSOR_COLUMNS:
        assert f"{col}_zscore" in anomalies_df.columns


def test_drift_z_columns_created(anomalies_df):
    for col in SENSOR_COLUMNS:
        assert f"{col}_drift_z" in anomalies_df.columns


def test_anomaly_flag_is_boolean(anomalies_df):
    for col in SENSOR_COLUMNS:
        assert anomalies_df[f"{col}_anomaly"].dtype == bool


def test_is_anomaly_consistent_with_anomaly_count(anomalies_df):
    # is_anomaly should be True iff anomaly_count > 0
    assert ((anomalies_df["anomaly_count"] > 0) == anomalies_df["is_anomaly"]).all()


def test_hvac_2_has_anomaly_rows(anomalies_df):
    """HVAC_2 should be flagged — it has two multi-sensor spike events."""
    h2 = anomalies_df[anomalies_df["unit_id"] == "HVAC_2"]
    assert h2["is_anomaly"].sum() >= 2


def test_hvac_2_has_multi_sensor_anomaly_row(anomalies_df):
    """HVAC_2 should have at least one row where 2+ sensors are anomalous simultaneously."""
    h2 = anomalies_df[anomalies_df["unit_id"] == "HVAC_2"]
    assert (h2["anomaly_count"] >= 2).any()


def test_hvac_3_has_anomaly_rows(anomalies_df):
    """HVAC_3 should be flagged — it has a sustained pressure drop in the last 3 hours."""
    h3 = anomalies_df[anomalies_df["unit_id"] == "HVAC_3"]
    assert h3["is_anomaly"].sum() > 0


def test_hvac_1_has_drift_anomaly(anomalies_df):
    """HVAC_1 should show sustained multi-sensor drift in the final hours."""
    h1 = anomalies_df[anomalies_df["unit_id"] == "HVAC_1"]
    assert h1["is_anomaly"].sum() >= 10, "Expected substantial drift anomaly in HVAC_1"


def test_hvac_5_has_minimal_anomalies(anomalies_df):
    """HVAC_5 should have very few anomalies — it is the cleanest unit."""
    h5 = anomalies_df[anomalies_df["unit_id"] == "HVAC_5"]
    assert h5["is_anomaly"].sum() <= 3


def test_anomalous_sensors_lists_are_lists(anomalies_df):
    for sensors in anomalies_df["anomalous_sensors"]:
        assert isinstance(sensors, list)


def test_anomalous_sensors_only_contains_valid_sensors(anomalies_df):
    valid = set(SENSOR_COLUMNS)
    for sensors in anomalies_df[anomalies_df["is_anomaly"]]["anomalous_sensors"]:
        assert set(sensors).issubset(valid)
