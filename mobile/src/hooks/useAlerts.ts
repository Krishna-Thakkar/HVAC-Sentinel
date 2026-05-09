import { useQuery } from '@tanstack/react-query';
import { fetchAlerts } from '../services/api';
import { QUERY_KEYS } from '../constants';

export function useAlerts() {
  return useQuery({
    queryKey: QUERY_KEYS.alerts,
    queryFn: fetchAlerts,
    refetchInterval: 30_000,  // poll every 30s for live alert updates
  });
}
