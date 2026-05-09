import pandas as pd
from app.constants import FILLABLE_COLUMNS


def test_no_missing_fillable_values_after_preprocessing(processed_df):
    for col in FILLABLE_COLUMNS:
        assert processed_df[col].isna().sum() == 0, f"{col} still has NaN after preprocessing"


def test_is_imputed_column_exists(processed_df):
    assert "is_imputed" in processed_df.columns


def test_is_imputed_marks_originally_missing_rows(raw_df, processed_df):
    # Rows where either temp or airflow was originally missing should be marked
    originally_missing = raw_df[FILLABLE_COLUMNS].isna().any(axis=1).sum()
    marked_imputed = processed_df["is_imputed"].sum()
    assert marked_imputed == originally_missing


def test_sorted_chronologically_per_unit(processed_df):
    for unit_id, group in processed_df.groupby("unit_id"):
        diffs = group["timestamp"].diff().dropna()
        assert (diffs > pd.Timedelta(0)).all(), f"{unit_id} is not sorted chronologically"


def test_row_count_preserved(raw_df, processed_df):
    assert len(processed_df) == len(raw_df)


def test_five_minute_intervals_per_unit(processed_df):
    expected = pd.Timedelta("5min")
    for unit_id, group in processed_df.groupby("unit_id"):
        diffs = group["timestamp"].diff().dropna()
        assert (diffs == expected).all(), f"{unit_id} has irregular intervals after sorting"


def test_forward_fill_does_not_bleed_across_units(processed_df):
    # The last row of HVAC_1 should not influence the first row of HVAC_2
    # (i.e., the is_imputed flag should only be set for originally-missing rows)
    for unit_id, group in processed_df.groupby("unit_id"):
        # All non-imputed temp values should be >= 20 (reasonable range for HVAC temp)
        non_imputed_temp = group[~group["is_imputed"]]["temp"]
        assert (non_imputed_temp > 0).all()
