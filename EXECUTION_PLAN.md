# HVAC Sentinel — Execution Plan

## Project Overview

HVAC Sentinel is an AI-powered mobile maintenance prioritization system for industrial HVAC monitoring.

The system helps maintenance technicians:
- reduce alert fatigue,
- identify high-risk HVAC systems,
- understand WHY issues matter,
- prioritize maintenance actions,
- suppress noisy alerts,
- receive AI-generated operational summaries.

The primary goal is NOT to build a dashboard.

The primary goal is to build a technician-first decision support system that improves trust in industrial alerting workflows.

This project is being developed for the AI Applied Engineer challenge.

---

# Core Product Philosophy

The application should answer:

> “Where should I go next and why?”

instead of:

> “What sensor data exists?”

The UX, AI explanations, anomaly detection, and prioritization logic should all reinforce this principle.

---

# Problem Statement

Manufacturing maintenance teams currently experience:
- excessive false alarms,
- alert fatigue,
- buried critical incidents,
- lack of trust in threshold-based systems.

The provided dataset contains:
- HVAC sensor telemetry,
- noisy signals,
- missing values,
- deceptive patterns.

The system should intelligently surface actionable incidents while suppressing low-confidence noise.

---

# Product Goals

## Primary Goals
- Reduce alert fatigue
- Surface actionable incidents
- Provide explainable AI summaries
- Prioritize technician attention
- Create mobile-first workflows

## Secondary Goals
- Demonstrate AI-native engineering workflow
- Showcase practical LLM integration
- Demonstrate strong product thinking
- Maintain clean architecture
- Ship quickly with iterative development

---

# Technical Philosophy

## AI Usage Principles

AI SHOULD be used for:
- summarization,
- recommendations,
- explanation,
- prioritization support,
- development acceleration.

AI SHOULD NOT be solely relied upon for:
- anomaly detection,
- deterministic calculations,
- core signal processing.

Core detection logic should remain deterministic and explainable.

---

# High-Level System Architecture

```text
Sensor Dataset
      ↓
Preprocessing Engine
      ↓
Feature Engineering
      ↓
Anomaly Detection Engine
      ↓
Incident Aggregation Engine
      ↓
AI Explanation Generator
      ↓
FastAPI Backend APIs
      ↓
React Native Mobile App
```

---

# Tech Stack

## Frontend
- React Native
- Expo
- TypeScript
- React Navigation
- React Query
- Recharts or lightweight chart library
- NativeWind or clean StyleSheet-based styling

## Backend
- FastAPI
- Python 3.11+
- Pandas
- NumPy
- Scikit-learn
- Uvicorn

## AI Layer
- OpenAI API or Claude API
- Prompt-engineered summaries
- Operational recommendations

## Tooling
- Claude Code
- ChatGPT
- Git
- GitHub

---

# Recommended Development Environment

- Node.js 20+
- Expo SDK 54
- Python 3.11+
- npm 10+

---

# Repository Structure

```text
/
├── EXECUTION_PLAN.md
├── README.md
├── backend/
│   ├── app/
│   ├── data/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
├── mobile/
│   ├── src/
│   ├── assets/
│   ├── package.json
│   └── README.md
│
├── datasets/
│   ├── raw/
│   ├── processed/
│   └── sample_outputs/
│
├── prompts/
│   ├── initialization/
│   ├── backend/
│   ├── frontend/
│   ├── ai/
│   ├── testing/
│   └── debugging/
│
├── docs/
│   ├── architecture/
│   ├── screenshots/
│   ├── diagrams/
│   └── demo/
│
└── assets/
```

---

# Data Management Strategy

## Raw Data
Store original untouched datasets under:

datasets/raw/

Raw datasets should never be modified directly.

## Processed Data
Store cleaned and feature-engineered datasets under:

datasets/processed/

Examples:
- normalized datasets
- anomaly-tagged datasets
- rolling statistics outputs

## Sample Outputs
Store reusable debugging/demo artifacts under:

datasets/sample_outputs/

Examples:
- sample API responses
- generated incidents
- screenshots metadata
- cached summaries

## Data Pipeline Principle
The preprocessing pipeline should always:
1. Read from datasets/raw/
2. Generate outputs into datasets/processed/
3. Never overwrite original datasets

---

# Core User Personas

## Maintenance Technician
Needs:
- fast prioritization,
- minimal noise,
- mobile-friendly UI,
- clear recommendations.

## Operations Lead
Needs:
- trust in alerts,
- reduced downtime,
- incident visibility,
- actionable summaries.

---

# Application Features

# Core Features (MVP)

## 1. HVAC Overview Dashboard
Displays:
- HVAC systems,
- health scores,
- risk levels,
- active incidents,
- suppressed alerts count,
- system status.

## 2. Incident Detail Screen
Displays:
- AI-generated explanation,
- severity,
- confidence,
- sensor trends,
- probable cause,
- recommended actions.

## 3. Alerts Feed
Displays:
- active alerts,
- grouped incidents,
- suppressed alerts,
- timestamps,
- reasoning.

## 4. AI Operational Summary
Generates:
- concise operational summaries,
- maintenance recommendations,
- incident explanations.

---

# Stretch Features (Optional)

## AI Assistant Chat
Technicians can ask:
- “Why is HVAC-2 critical?”
- “What changed recently?”
- “What should I inspect first?”

## Predictive Failure Estimation
Estimate:
- possible failure windows,
- maintenance urgency.

## Historical Incident Trends
View:
- recurring incidents,
- repeated anomalies.

---

# Backend Architecture

# Backend Modules

## data_loader.py
Responsibilities:
- load datasets from datasets/raw/,
- validate file schema,
- support reproducible preprocessing pipeline.

## preprocessing.py
Responsibilities:
- handle missing values,
- normalize data,
- rolling statistics.

## feature_engineering.py
Responsibilities:
- generate:
  - rolling averages,
  - trend slopes,
  - rate-of-change metrics,
  - vibration deltas.

## anomaly_detection.py
Responsibilities:
- z-score anomalies,
- rolling deviation analysis,
- optional Isolation Forest.

## incident_engine.py
Responsibilities:
- group anomalies,
- assign severity,
- suppress noise,
- generate confidence scores.

## ai_summary.py
Responsibilities:
- generate operational summaries,
- maintenance recommendations,
- human-readable explanations.

## routes/
FastAPI routes.

---

# API Design

# GET /systems

Returns:
- HVAC overview data,
- health scores,
- incident counts.

# GET /systems/{id}

Returns:
- detailed system data,
- incidents,
- charts,
- AI summary.

# GET /alerts

Returns:
- active alerts,
- suppressed alerts,
- incident timeline.

# POST /assistant

Optional conversational AI endpoint.

---

# Frontend Architecture

# Mobile Folder Structure

```text
mobile/src/
├── screens/
├── components/
├── services/
├── hooks/
├── types/
├── constants/
├── navigation/
├── utils/
└── theme/
```

---

# Mobile Screens

# 1. Overview Screen
Purpose:
Quick system prioritization.

UI Elements:
- HVAC cards,
- risk badges,
- health score,
- active alerts count.

# 2. System Detail Screen
Purpose:
Deep inspection.

UI Elements:
- AI explanation,
- sensor graphs,
- recommendation cards,
- incident timeline.

# 3. Alerts Screen
Purpose:
Alert visibility and transparency.

UI Elements:
- grouped alerts,
- suppressed alerts,
- timestamps,
- severity filters.

# 4. Assistant Screen (Optional)
Purpose:
Natural-language operational assistance.

---

# UI/UX Guidelines

## Design Philosophy
- industrial,
- minimal,
- operational,
- readable,
- mobile-first.

## Avoid
- excessive animations,
- clutter,
- startup-style gradients,
- unnecessary charts.

## Prioritize
- readability,
- large touch targets,
- quick scanning,
- concise copy,
- technician usability.

---

# Anomaly Detection Strategy

# Goal
Reduce noisy alerts while surfacing actionable incidents.

# Detection Pipeline

## Step 1 — Preprocessing
- handle missing values,
- clean timestamps,
- sort chronologically.

## Step 2 — Feature Engineering
Generate:
- rolling averages,
- rolling std deviation,
- trend slopes,
- vibration spikes,
- airflow-pressure mismatches.

## Step 3 — Anomaly Detection
Methods:
- z-score analysis,
- rolling deviation thresholds,
- optional Isolation Forest.

## Step 4 — Incident Aggregation
Combine:
- correlated anomalies,
- duration,
- severity,
- confidence.

A single noisy spike should NOT trigger a major incident.

---

# AI Layer Design

# AI Responsibilities
- explain incidents,
- summarize operational risk,
- recommend actions,
- convert technical signals into technician-friendly language.

# AI Prompting Principles
- concise,
- operational,
- actionable,
- avoid hallucinations,
- avoid overconfidence.

# Example Output

“HVAC-3 shows sustained vibration increases alongside reduced airflow efficiency over the last 4 hours. This pattern may indicate bearing wear or airflow obstruction. Inspection recommended within the next maintenance cycle.”

---

# Testing Strategy

# Backend Testing
- API tests,
- anomaly logic tests,
- preprocessing tests.

# Frontend Testing
- screen rendering,
- navigation flow,
- API integration.

# Manual Validation
- verify AI outputs,
- verify incident prioritization,
- verify mobile usability.

---

# Coding Standards

## General
- modular architecture,
- reusable components,
- typed interfaces,
- clean naming conventions.

## Backend
- typed Python functions,
- separation of concerns,
- minimal business logic in routes.

## Frontend
- reusable UI components,
- clean hooks-based architecture,
- strongly typed props/interfaces.

---

# AI-Native Development Workflow

This project intentionally uses AI-assisted development.

Claude Code and ChatGPT should be used for:
- scaffolding,
- implementation,
- debugging,
- documentation,
- architecture refinement.

Human oversight is REQUIRED for:
- architecture decisions,
- logic validation,
- UX coherence,
- technical correctness.

---

# Git & Version Control Workflow

Each completed phase should include:
- a semantic git commit message,
- a concise implementation summary,
- updated execution checklist items,
- documented blockers/issues if applicable.

## Commit Message Format

Use semantic commit conventions:

- feat: new functionality
- fix: bug fixes
- refactor: code restructuring
- docs: documentation updates
- chore: tooling/setup/configuration
- test: testing-related updates

## Commit Workflow

At the end of each phase:
1. Generate recommended semantic commit message
2. Commit completed work
3. Push to remote repository
4. Update EXECUTION_PLAN.md progress
5. Document implementation notes and blockers

## Commit History

### Phase 0
chore: initialize HVAC Sentinel project scaffold
docs: update execution plan and development workflow

---

# Claude Code Operating Instructions

Before making changes:
1. Read EXECUTION_PLAN.md completely.
2. Follow defined architecture and folder structure.
3. Do not introduce unnecessary complexity.
4. Keep implementation modular and maintainable.
5. Prefer clarity over cleverness.

After completing tasks:
1. Update task checklist
2. Add implementation notes
3. Add blockers/issues if any
4. Suggest improvements separately
5. Do not modify unrelated files
6. Generate a semantic git commit message
7. Summarize completed architectural changes

---

# Phase Breakdown

# PHASE 0 — Planning & Setup

## Goals
- initialize repository,
- create folder structure,
- finalize architecture,
- prepare dataset ingestion.

## Deliverables
- repo scaffold,
- initial README,
- execution plan,
- environment setup.

## Checklist
- [x] Create repository structure
- [x] Setup backend folder
- [x] Setup Expo React Native app
- [x] Configure Git
- [x] Add environment variable support (.env.example created)
- [x] Add requirements.txt
- [x] Add package.json dependencies
- [x] Create prompts directory
- [x] Create datasets/raw directory
- [x] Move original dataset into datasets/raw
- [x] Create datasets/processed directory
- [x] Create datasets/sample_outputs directory
- [x] Validate dataset schema (see backend/data/dataset_report.md)

---

# PHASE 1 — Backend Foundation

## Goals
- ingest dataset,
- preprocess data,
- generate anomaly signals,
- expose APIs.

## Deliverables
- FastAPI app,
- preprocessing pipeline,
- anomaly engine,
- API endpoints.

## Checklist
- [ ] Implement dataset loader
- [ ] Implement preprocessing
- [ ] Implement feature engineering
- [ ] Implement anomaly detection
- [ ] Implement incident aggregation
- [ ] Implement FastAPI routes
- [ ] Add backend tests
- [ ] Validate API responses

---

# PHASE 2 — Mobile Foundation

## Goals
- initialize mobile app,
- setup navigation,
- connect APIs.

## Deliverables
- Expo app,
- navigation system,
- API integration layer.

## Checklist
- [ ] Setup navigation
- [ ] Setup folder structure
- [ ] Create API services
- [ ] Create reusable UI components
- [ ] Configure theming
- [ ] Add loading/error states

---

# PHASE 3 — Core Product Features

## Goals
- implement technician workflows,
- build prioritization UI,
- display operational intelligence.

## Deliverables
- overview screen,
- detail screen,
- alerts feed.

## Checklist
- [ ] Build Overview Screen
- [ ] Build System Detail Screen
- [ ] Build Alerts Screen
- [ ] Add charts
- [ ] Add health indicators
- [ ] Add incident cards

---

# PHASE 4 — AI Features

## Goals
- generate explainable summaries,
- operational recommendations.

## Deliverables
- AI summaries,
- recommendation engine,
- optional assistant.

## Checklist
- [ ] Build AI summary prompts
- [ ] Integrate LLM APIs
- [ ] Add recommendation generation
- [ ] Add assistant endpoint
- [ ] Validate output quality

---

# PHASE 5 — Polish & Stabilization

## Goals
- improve UX,
- improve reliability,
- finalize visuals.

## Deliverables
- polished UX,
- improved responsiveness,
- stable APIs.

## Checklist
- [ ] Improve UI consistency
- [ ] Improve loading states
- [ ] Improve responsiveness
- [ ] Remove dead code
- [ ] Refactor reusable logic
- [ ] Final QA pass

---

# PHASE 6 — Submission Assets

## Goals
- finalize documentation,
- prepare demo assets,
- create walkthrough.

## Deliverables
- final README,
- screenshots,
- architecture diagrams,
- walkthrough video.

## Checklist
- [ ] Write final README
- [ ] Add architecture diagrams
- [ ] Capture screenshots
- [ ] Record walkthrough video
- [ ] Final repository cleanup

---

# README Requirements

README should include:
- project overview,
- problem statement,
- architecture,
- AI usage,
- anomaly detection strategy,
- tradeoffs,
- setup instructions,
- screenshots,
- future improvements.

README should emphasize:
- product thinking,
- AI-native workflow,
- operational value.

---

# Demo Video Requirements

Duration:
2–3 minutes.

Must Cover:
- problem understanding,
- architecture,
- anomaly logic,
- AI summaries,
- mobile workflows,
- tradeoffs,
- future improvements.

Avoid:
- scripted marketing language,
- feature dumping.

Focus on:
- thinking process,
- operational usefulness,
- AI engineering workflow.

---

# Success Criteria

The project succeeds if:
- the app feels useful to technicians,
- alert fatigue is visibly addressed,
- AI explanations improve clarity,
- architecture remains clean,
- the system demonstrates strong product thinking,
- the implementation feels practical and believable.

---

# Implementation Notes

## Phase 0 — 2026-05-09

- Repository structure created per EXECUTION_PLAN.md specification.
- Backend: FastAPI scaffold initialized with modular architecture including `main.py`, `config.py`, route stubs for `/health`, `/systems`, and `/alerts`. Backend APIs verified locally using Uvicorn.
- Mobile: Expo React Native TypeScript scaffold initialized using React Navigation architecture. Navigation, theme system, hooks, API client structure, and typed interfaces are configured.
- Frontend environment upgraded and stabilized on Expo SDK 54 with Node.js 20+ for Expo Go compatibility.
- Removed `expo-router` configuration in favor of a simpler React Navigation setup to avoid mixed navigation architectures.
- Expo dependency ecosystem stabilized after SDK migration and dependency reconciliation.
- Mobile application rendering and navigation verified successfully on a physical Android device using Expo Go.
- Dataset analysis complete — see `backend/data/dataset_report.md`.
- Key dataset findings:
  - HVAC_2 shows multi-sensor anomalies (temperature, airflow, vibration)
  - HVAC_3 shows sustained pressure deviation
  - Single-row spikes exist and should be suppressed during incident aggregation
  - Missing airflow and temperature values support per-unit forward-fill preprocessing
- These observations should guide Phase 1 anomaly detection and incident aggregation logic.
- Semantic git workflow established for phased development tracking.
- Initial repository baseline committed and pushed:
  - `chore: initialize HVAC Sentinel project scaffold`
- A temporary `.venv/` was created in the root for dataset analysis — it is gitignored and can be removed if desired.



# Blockers / Issues

## Phase 0

- **Node.js version** — System Node is 14.20.0. Expo SDK 52 requires Node 18+. Mobile app cannot be installed or run until Node is upgraded. Recommend: install `nvm`, then `nvm install 18 && nvm use 18`.
- **Git not initialized** — Run `git init && git add . && git commit -m "Phase 0: initial scaffold"` from the project root to begin tracking history.

---

# Future Improvements

(To be updated continuously during development.)