/**
 * React Query hook for fetching the latest lottery result
 */

import { useQuery } from "@tanstack/react-query";
import { api } from "@/services/api";
import type { LatestResult } from "@/types/api";

export function useLatestResult() {
  return useQuery<LatestResult, Error>({
    queryKey: ["latest-result"],
    queryFn: () => api.getLatestResult(),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
    retry: 2,
  });
}
