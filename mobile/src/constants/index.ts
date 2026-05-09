// Replace with your machine's IP when testing on a physical device
// For Android emulator: http://10.0.2.2:8000
// For iOS simulator or web: http://localhost:8000
export const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000';

export const SEVERITY_LABELS: Record<string, string> = {
  critical: 'CRITICAL',
  warning: 'WARNING',
  normal: 'NORMAL',
  info: 'INFO',
};

export const QUERY_KEYS = {
  systems: ['systems'] as const,
  system: (id: string) => ['systems', id] as const,
  alerts: ['alerts'] as const,
};
