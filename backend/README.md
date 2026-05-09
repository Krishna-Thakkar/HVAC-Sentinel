# HVAC Sentinel — Backend

FastAPI backend for the HVAC Sentinel maintenance prioritization system.

## Structure

```
backend/
├── main.py              # FastAPI app entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── app/
│   ├── config.py        # Settings loaded from .env
│   ├── routes/          # API route handlers
│   │   ├── health.py    # Health check
│   │   ├── systems.py   # HVAC system endpoints
│   │   └── alerts.py    # Alert feed endpoints
│   ├── services/        # Business logic (Phase 1+)
│   ├── models/          # Pydantic response models (Phase 1+)
│   └── utils/           # Shared utilities (Phase 1+)
├── data/                # Dataset reports and processed artifacts
└── tests/               # Pytest test suite
```

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Fill in your API keys
```

## Run

```bash
uvicorn main:app --reload
# API available at: http://localhost:8000
# Docs available at: http://localhost:8000/docs
```

## Test

```bash
pytest tests/
```

## Phase Status

| Phase | Status |
|---|---|
| Phase 0 — Setup | Complete |
| Phase 1 — Backend Foundation | Pending |
| Phase 4 — AI Features | Pending |
