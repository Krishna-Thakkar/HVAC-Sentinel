from typing import Final

# ---------------------------------------------------------------------------
# Time series
# ---------------------------------------------------------------------------

# 10 readings at 5-minute intervals = 50-minute rolling window
ROLLING_WINDOW: Final[int] = 10
# Minimum readings before rolling stats are considered reliable
MIN_ROLLING_PERIODS: Final[int] = 3

# ---------------------------------------------------------------------------
# Anomaly detection
# ---------------------------------------------------------------------------

# A sensor reading is anomalous if its rolling z-score exceeds this magnitude
Z_SCORE_THRESHOLD: Final[float] = 2.5

# A sensor's rolling mean is drifting if it deviates from the unit's overall median
# by more than this many multiples of the unit's overall std deviation.
# Detects sustained level shifts that rolling z-scores miss (they adapt to the new level).
DRIFT_Z_THRESHOLD: Final[float] = 2.0

# ---------------------------------------------------------------------------
# Incident aggregation (incident_engine)
# ---------------------------------------------------------------------------

# Minimum consecutive anomalous rows to form a real incident (duration gating).
# Runs shorter than this are marked suppressed — isolated noise.
MIN_INCIDENT_ROWS: Final[int] = 2

# Minimum sensors simultaneously flagged to bypass duration gating (incident not suppressed)
CRITICAL_SENSOR_COUNT: Final[int] = 2

# Minimum sensors simultaneously flagged in a SINGLE ROW to elevate severity to CRITICAL.
# Requires stronger corroboration than the suppression bypass — 3+ sensors at once
# represents a compelling multi-system failure signal.
CRITICAL_SIMULTANEOUS_SENSORS: Final[int] = 3

# >= this many consecutive anomaly rows in a run → CRITICAL severity
CRITICAL_DURATION_ROWS: Final[int] = 4

# ---------------------------------------------------------------------------
# Confidence scoring
# ---------------------------------------------------------------------------

# Row count at which a run achieves maximum duration-based confidence
CONFIDENCE_MAX_ROWS: Final[int] = 8
# Floor confidence for any incident that passes duration gating
CONFIDENCE_MIN: Final[float] = 0.30

# ---------------------------------------------------------------------------
# Health score computation
# ---------------------------------------------------------------------------

# Point deductions per active incident (applied after density penalty)
HEALTH_PENALTY_CRITICAL: Final[int] = 20
HEALTH_PENALTY_WARNING: Final[int] = 10
# Weight applied to anomaly-row density (0–1 ratio → 0–WEIGHT penalty points)
HEALTH_DENSITY_WEIGHT: Final[float] = 40.0

# ---------------------------------------------------------------------------
# Sensor columns (order matters — used in feature engineering and detection)
# ---------------------------------------------------------------------------

SENSOR_COLUMNS: Final[list[str]] = ["temp", "pressure", "airflow", "vibration", "power"]

# Columns with natural missing values that should be forward-filled
FILLABLE_COLUMNS: Final[list[str]] = ["temp", "airflow"]
