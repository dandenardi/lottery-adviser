/**
 * React Query hook for fetching lottery statistics
 */

import { useQuery } from "@tanstack/react-query";
import { api } from "@/services/api";
import type { Statistics } from "@/types/api";

export function useStatistics() {
  return useQuery<Statistics, Error>({
    queryKey: ["statistics"],
    queryFn: () => api.getStatistics(),
    staleTime: 30 * 60 * 1000, // 30 minutes
    gcTime: 60 * 60 * 1000, // 1 hour
    retry: 2,
  });
}
