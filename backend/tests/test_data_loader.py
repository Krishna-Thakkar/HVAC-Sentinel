import pytest
from app.services.data_loader import load_raw_data
from app.constants import SENSOR_COLUMNS


def test_loads_without_error(raw_df):
    assert raw_df is not None


def test_row_count(raw_df):
    assert len(raw_df) == 1000


def test_required_columns(raw_df):
    required = {"timestamp", "unit_id"} | set(SENSOR_COLUMNS)
    assert required.issubset(set(raw_df.columns))


def test_five_units(raw_df):
    assert set(raw_df["unit_id"].unique()) == {"HVAC_1", "HVAC_2", "HVAC_3", "HVAC_4", "HVAC_5"}


def test_balanced_unit_distribution(raw_df):
    counts = raw_df["unit_id"].value_counts()
    assert (counts == 200).all()


def test_timestamps_are_datetime(raw_df):
    import pandas as pd
    assert pd.api.types.is_datetime64_any_dtype(raw_df["timestamp"])


def test_no_negative_sensor_values(raw_df):
    for col in SENSOR_COLUMNS:
        assert (raw_df[col].dropna() >= 0).all(), f"{col} has negative values"


def test_no_duplicate_unit_timestamps(raw_df):
    dups = raw_df.duplicated(subset=["timestamp", "unit_id"]).sum()
    assert dups == 0


def test_known_missing_columns(raw_df):
    # Dataset validation: only temp and airflow have missing values
    assert raw_df["temp"].isna().sum() > 0, "Expected missing temp values"
    assert raw_df["airflow"].isna().sum() > 0, "Expected missing airflow values"
    assert raw_df["pressure"].isna().sum() == 0
    assert raw_df["vibration"].isna().sum() == 0
    assert raw_df["power"].isna().sum() == 0
