import pandas as pd
from pathlib import Path

from app.constants import SENSOR_COLUMNS

# Resolve paths relative to this file so they work regardless of cwd
_SERVICES_DIR = Path(__file__).parent
_BACKEND_DIR = _SERVICES_DIR.parent.parent
_PROJECT_ROOT = _BACKEND_DIR.parent

RAW_DATA_PATH = _PROJECT_ROOT / "datasets" / "raw" / "hvac_sensor_data.csv"
PROCESSED_DIR = _PROJECT_ROOT / "datasets" / "processed"

REQUIRED_COLUMNS = {"timestamp", "unit_id"} | set(SENSOR_COLUMNS)


def load_raw_data() -> pd.DataFrame:
    """Load and validate the raw HVAC sensor CSV dataset."""
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at: {RAW_DATA_PATH}")

    df = pd.read_csv(RAW_DATA_PATH, parse_dates=["timestamp"])

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    if df.empty:
        raise ValueError("Dataset is empty.")

    return df


def save_processed(df: pd.DataFrame, name: str) -> Path:
    """Persist a pipeline-stage DataFrame to datasets/processed/{name}.csv."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DIR / f"{name}.csv"
    df.to_csv(output_path, index=False)
    return output_path
