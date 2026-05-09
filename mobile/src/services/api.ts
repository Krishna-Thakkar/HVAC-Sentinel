import axios from 'axios';
import { API_BASE_URL } from '../constants';
import type { HvacSystem, Incident, Alert, ApiResponse } from '../types';

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10_000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Phase 1 — these will return real data once the backend is implemented

export async function fetchSystems(): Promise<HvacSystem[]> {
  const res = await client.get<ApiResponse<HvacSystem[]>>('/systems');
  return res.data.data;
}

export async function fetchSystem(id: string): Promise<HvacSystem & { incidents: Incident[] }> {
  const res = await client.get(`/systems/${id}`);
  return res.data.data;
}

export async function fetchAlerts(): Promise<Alert[]> {
  const res = await client.get<ApiResponse<Alert[]>>('/alerts');
  return res.data.data;
}

export async function checkHealth(): Promise<{ status: string }> {
  const res = await client.get('/health');
  return res.data;
}
