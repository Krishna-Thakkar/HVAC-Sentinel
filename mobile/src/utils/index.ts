import type { SeverityLevel } from '../types';
import { colors } from '../theme/theme';

export function severityColor(severity: SeverityLevel): string {
  return colors.severity[severity] ?? colors.severity.info;
}

export function formatTimestamp(iso: string): string {
  const date = new Date(iso);
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export function healthScoreLabel(score: number): SeverityLevel {
  if (score >= 80) return 'normal';
  if (score >= 50) return 'warning';
  return 'critical';
}
