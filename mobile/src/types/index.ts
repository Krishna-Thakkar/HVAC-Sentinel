// Core domain types for HVAC Sentinel
// Expanded in Phase 1 as API contracts are finalized

export type SeverityLevel = 'critical' | 'warning' | 'normal' | 'info';

export interface HvacSystem {
  id: string;
  name: string;
  healthScore: number;        // 0–100
  severity: SeverityLevel;
  activeIncidentCount: number;
  suppressedAlertCount: number;
  lastUpdated: string;        // ISO timestamp
}

export interface SensorReading {
  timestamp: string;
  temp: number | null;
  pressure: number;
  airflow: number | null;
  vibration: number;
  power: number;
}

export interface Incident {
  id: string;
  systemId: string;
  severity: SeverityLevel;
  confidence: number;         // 0.0–1.0
  startedAt: string;
  summary: string;            // AI-generated
  probableCause: string;      // AI-generated
  recommendation: string;     // AI-generated
  sensors: string[];          // which sensors triggered this
}

export interface Alert {
  id: string;
  systemId: string;
  sensor: string;
  severity: SeverityLevel;
  value: number;
  threshold: number;
  timestamp: string;
  suppressed: boolean;
  reason?: string;            // suppression reason
}

// API response wrappers
export interface ApiResponse<T> {
  data: T;
  timestamp: string;
}

export interface ApiError {
  message: string;
  code?: string;
}
