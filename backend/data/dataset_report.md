# HVAC Sentinel — Dataset Validation Report

Generated: Phase 0 — Planning & Setup  
Source file: `datasets/raw/hvac_sensor_data.csv`

---

## Schema

| Column | Type | Notes |
|---|---|---|
| `timestamp` | datetime | UTC, 5-minute intervals |
| `unit_id` | string | HVAC unit identifier |
| `temp` | float | Temperature (°C assumed) |
| `pressure` | float | System pressure |
| `airflow` | float | Airflow rate (CFM assumed) |
| `vibration` | float | Vibration amplitude |
| `power` | float | Power consumption (kW assumed) |

---

## Dataset Shape

- **Total rows:** 1,000
- **Total columns:** 7
- **HVAC units:** 5 (HVAC_1 through HVAC_5)
- **Rows per unit:** 200 (perfectly balanced)

---

## Timestamp Coverage

| Property | Value |
|---|---|
| Start | 2026-01-01 00:00:00 |
| End | 2026-01-01 16:35:00 |
| Duration | 16 hours 35 minutes |
| Interval | 5 minutes (perfectly regular, no gaps) |
| Total timesteps per unit | 200 |

All 5 units share identical timestamps. No timestamp gaps detected per unit.

> Note: The dataset represents a single operational day (simulated).
> Phase 1 preprocessing should normalize timestamps relative to each unit's start time.

---

## Missing Values

| Column | Missing Count | Missing % |
|---|---|---|
| timestamp | 0 | 0.0% |
| unit_id | 0 | 0.0% |
| **temp** | **137** | **13.7%** |
| pressure | 0 | 0.0% |
| **airflow** | **147** | **14.7%** |
| vibration | 0 | 0.0% |
| power | 0 | 0.0% |

**Key observation:** `temp` and `airflow` both have ~14% missing values. This is realistic noise in industrial sensor data.

Preprocessing strategy (Phase 1):
- Forward-fill (ffill) then backward-fill (bfill) within each unit's time series
- Flag imputed rows for downstream confidence scoring
- Never drop rows — maintain time series continuity

---

## Descriptive Statistics

| Metric | temp | pressure | airflow | vibration | power |
|---|---|---|---|---|---|
| Mean | 22.15 | 1.19 | 315.23 | 0.027 | 5.15 |
| Std | 0.84 | 0.08 | 19.10 | 0.027 | 0.66 |
| Min | 21.03 | 0.68 | 119.60 | 0.004 | 4.41 |
| Max | 37.01 | 1.39 | 334.75 | 0.222 | 9.08 |

**Notable ranges:**
- `temp`: Normal ~22°C, max spike to 37°C (+70% above normal — strong signal)
- `airflow`: Normal ~315 CFM, min drop to 119 CFM (−62% — critical drop signal)
- `vibration`: Normal ~0.021, max spike to 0.222 (10x normal — strong anomaly signal)
- `power`: Normal ~5.1 kW, max to 9.1 kW (78% above normal)

No negative values detected. No duplicate (timestamp, unit_id) pairs.

---

## Anomaly Signal Preview (3-sigma per unit)

| Unit | Sensor | Flagged Rows |
|---|---|---|
| HVAC_1 | pressure | 1 |
| HVAC_2 | temp | 1 |
| HVAC_2 | airflow | 2 |
| HVAC_2 | vibration | 2 |
| HVAC_3 | pressure | 4 |
| HVAC_3 | power | 1 |
| HVAC_4 | temp | 1 |
| HVAC_4 | pressure | 1 |
| HVAC_4 | airflow | 1 |
| HVAC_5 | temp | 1 |

**Key observation:** HVAC_2 has multi-sensor anomalies (temp + airflow + vibration simultaneously), making it the highest-priority unit for incident detection.  
HVAC_3 has persistent pressure deviation (4 rows), suggesting a sustained anomaly rather than a transient spike.

---

## Preprocessing Concerns

| Concern | Impact | Recommended Handling |
|---|---|---|
| 13.7% missing `temp` | Medium | Forward-fill per unit, flag imputed rows |
| 14.7% missing `airflow` | High | Forward-fill per unit, flag imputed rows |
| Extreme `airflow` drop (119 CFM) | High | Z-score detection, duration-gating |
| Extreme `vibration` spike (0.222) | High | Rolling std deviation check |
| Single-row outliers (most units) | Low | Suppress unless sustained ≥ 2 readings |
| Dataset covers 1 day only | Medium | Rolling windows must be unit-scoped |

---

## Phase 1 Recommendations

1. Implement per-unit forward-fill for `temp` and `airflow`
2. Add `is_imputed` boolean flag column after fill
3. Compute rolling 10-window (50 min) mean and std per sensor per unit
4. Use per-unit z-scores (not global) for anomaly detection
5. Require ≥ 2 consecutive anomaly readings to trigger an incident
6. HVAC_2 and HVAC_3 are the most likely sources of real incidents in this dataset

---

## Data Quality Summary

| Dimension | Assessment |
|---|---|
| Completeness | Good — only 2 of 5 sensors have missing values |
| Consistency | Excellent — no duplicates, no negatives, regular timestamps |
| Anomaly richness | Good — detectable spikes and drops across multiple units |
| Temporal coverage | Limited — 16.5 hours is sufficient for rolling window analysis |
| Unit balance | Perfect — 200 rows per unit |
