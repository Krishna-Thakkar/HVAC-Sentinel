# HVAC Sentinel

An AI-powered mobile maintenance prioritization system for industrial HVAC monitoring.

> "Where should I go next and why?"

---

## Problem

Manufacturing maintenance teams face:
- excessive false alarms and alert fatigue,
- buried critical incidents in noisy threshold-based systems,
- lack of explainability in automated alerting,
- no clear answer to: *what should I inspect first?*

---

## Solution

HVAC Sentinel is a technician-first decision support system that:
- detects anomalies deterministically using sensor telemetry,
- aggregates correlated signals into actionable incidents,
- suppresses noisy low-confidence alerts,
- generates AI-powered operational summaries that explain *why* something matters,
- surfaces a prioritized work queue for maintenance teams.

---

## Architecture

```
Sensor Dataset (CSV)
      ↓
Preprocessing Engine      — handle missing values, normalize, rolling stats
      ↓
Feature Engineering       — rolling averages, trend slopes, vibration deltas
      ↓
Anomaly Detection Engine  — z-score + rolling deviation (deterministic)
      ↓
Incident Aggregation      — group correlated anomalies, assign severity/confidence
      ↓
AI Explanation Generator  — LLM-powered operational summaries
      ↓
FastAPI Backend APIs      — /systems, /alerts, /assistant
      ↓
React Native Mobile App   — Overview, Detail, Alerts screens
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Mobile | React Native + Expo + TypeScript |
| Backend | FastAPI + Python 3.11+ |
| Data Processing | Pandas + NumPy + Scikit-learn |
| AI | OpenAI API (or Claude API) |
| Navigation | React Navigation v6 |
| Data Fetching | React Query (TanStack) |

---

## AI Usage

AI is used **only** for:
- generating operational summaries,
- explaining incident root causes,
- recommending maintenance actions.

AI is **not** used for anomaly detection — that remains fully deterministic and explainable.

---

## Anomaly Detection Strategy

1. **Preprocessing** — forward-fill missing `temp`/`airflow` values per unit
2. **Feature Engineering** — rolling 10-window means, std deviations, trend slopes
3. **Detection** — per-unit z-scores (≥ 3σ) across temp, pressure, airflow, vibration, power
4. **Incident Gating** — require ≥ 2 consecutive anomaly readings to suppress single-point noise
5. **Severity** — multi-sensor correlation elevates severity to critical

---

## Repository Structure

```
/
├── EXECUTION_PLAN.md        # Full project execution plan
├── README.md
├── .gitignore
├── backend/                 # FastAPI backend
│   ├── main.py
│   ├── app/
│   │   ├── config.py
│   │   ├── routes/          # health, systems, alerts
│   │   ├── services/        # data_loader, preprocessing, anomaly_detection, etc.
│   │   ├── models/          # Pydantic response schemas
│   │   └── utils/
│   ├── data/                # Dataset reports
│   ├── tests/
│   └── requirements.txt
├── mobile/                  # Expo React Native app
│   ├── App.tsx
│   └── src/
│       ├── screens/
│       ├── components/
│       ├── services/        # API client
│       ├── hooks/           # React Query hooks
│       ├── navigation/
│       ├── types/
│       ├── theme/
│       └── constants/
├── datasets/
│   ├── raw/                 # Original unmodified dataset
│   ├── processed/           # Pipeline outputs
│   └── sample_outputs/      # Cached API responses, screenshots metadata
├── docs/
│   ├── architecture/
│   ├── diagrams/
│   └── demo/
└── prompts/                 # AI prompt templates used in development
```

---

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env         # add API keys
uvicorn main:app --reload
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Mobile

> Requires Node.js 18+

```bash
cd mobile
npm install
npm start                    # or: expo start
```

Set your backend URL in `mobile/.env`:
```
EXPO_PUBLIC_API_URL=http://localhost:8000
```

---

## Development Roadmap

| Phase | Goal | Status |
|---|---|---|
| 0 — Setup | Repository scaffold, environment | Complete |
| 1 — Backend Foundation | Data pipeline, anomaly engine, APIs | Pending |
| 2 — Mobile Foundation | Navigation, API integration | Pending |
| 3 — Core Product | Overview, Detail, Alerts screens | Pending |
| 4 — AI Features | LLM summaries, recommendations | Pending |
| 5 — Polish | UX refinement, stability | Pending |
| 6 — Submission | Docs, screenshots, demo video | Pending |

---

## Dataset

Source: `datasets/raw/hvac_sensor_data.csv`

- 5 HVAC units (HVAC_1 through HVAC_5)
- 200 readings per unit at 5-minute intervals
- Covers 16.5 hours of simulated operational data
- Sensors: temperature, pressure, airflow, vibration, power
- ~14% missing values in temp and airflow (realistic industrial noise)
- See `backend/data/dataset_report.md` for full analysis

---

## Future Improvements

- Real-time WebSocket streaming for live sensor updates
- Predictive failure window estimation
- Historical trend views and recurring incident detection
- AI assistant chat for natural-language operational queries
- Push notifications for critical incidents
