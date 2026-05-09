# HVAC Sentinel — Mobile App

Expo React Native (TypeScript) mobile app for HVAC Sentinel.

## Requirements

- Node.js 18+ (Node 14 detected on this machine — upgrade required before running)
- npm or yarn
- Expo CLI: `npm install -g expo-cli`
- For device testing: Expo Go app

## Structure

```
mobile/
├── App.tsx                  # App entry — QueryClient + NavigationContainer
├── app.json                 # Expo configuration
├── tsconfig.json            # TypeScript config with path aliases (@/*)
├── babel.config.js
├── src/
│   ├── screens/             # Full-page screen components (Phase 3)
│   ├── components/          # Reusable UI components (Phase 3)
│   ├── services/
│   │   └── api.ts           # Axios API client
│   ├── hooks/
│   │   ├── useSystems.ts    # React Query hooks for HVAC systems
│   │   └── useAlerts.ts     # React Query hooks for alerts
│   ├── navigation/
│   │   ├── RootNavigator.tsx
│   │   └── types.ts         # Stack/tab param list types
│   ├── types/
│   │   └── index.ts         # Domain type definitions
│   ├── constants/
│   │   └── index.ts         # API URL, query keys, labels
│   ├── theme/
│   │   └── theme.ts         # Color palette, spacing, typography
│   └── utils/
│       └── index.ts         # Formatting and helper functions
└── assets/                  # Images and icons
```

## Setup

```bash
cd mobile
npm install
npm start          # or: expo start
```

## Environment

Create a `.env` file in `mobile/`:
```
EXPO_PUBLIC_API_URL=http://localhost:8000
```

For physical device testing, replace `localhost` with your machine's local IP.

## Phase Status

| Phase | Status |
|---|---|
| Phase 0 — Scaffold | Complete |
| Phase 2 — Navigation & API | Pending |
| Phase 3 — Core Screens | Pending |
| Phase 4 — AI Features | Pending |
