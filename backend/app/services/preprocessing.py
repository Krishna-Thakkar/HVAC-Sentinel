import pandas as pd

from app.constants import FILLABLE_COLUMNS


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and normalize raw HVAC sensor data.

    Steps:
      1. Parse timestamps and sort chronologically per unit.
      2. Record which rows had originally missing sensor values (is_imputed).
      3. Forward-fill then backward-fill fillable sensor columns per unit —
         preserves time-series continuity without introducing future information.
    """
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(["unit_id", "timestamp"]).reset_index(drop=True)

    # Mark rows that had at least one fillable column missing before filling.
    df["is_imputed"] = df[FILLABLE_COLUMNS].isna().any(axis=1)

    # Per-unit fill using transform — avoids groupby.apply deprecation and is vectorized.
    # Fills each sensor independently within its unit boundary.
    for col in FILLABLE_COLUMNS:
        df[col] = df.groupby("unit_id")[col].transform(lambda x: x.ffill().bfill())

    return df.reset_index(drop=True)
