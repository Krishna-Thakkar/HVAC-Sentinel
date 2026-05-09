import { useQuery } from '@tanstack/react-query';
import { fetchSystems, fetchSystem } from '../services/api';
import { QUERY_KEYS } from '../constants';

export function useSystems() {
  return useQuery({
    queryKey: QUERY_KEYS.systems,
    queryFn: fetchSystems,
  });
}

export function useSystem(id: string) {
  return useQuery({
    queryKey: QUERY_KEYS.system(id),
    queryFn: () => fetchSystem(id),
    enabled: Boolean(id),
  });
}
