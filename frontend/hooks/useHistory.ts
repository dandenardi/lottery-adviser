/**
 * React Query hook for fetching lottery history with pagination
 */

import { useInfiniteQuery } from "@tanstack/react-query";
import { api } from "@/services/api";
import type { HistoryResponse } from "@/types/api";

const PAGE_SIZE = 20;

export function useHistory() {
  return useInfiniteQuery<HistoryResponse, Error>({
    queryKey: ["history"],
    queryFn: ({ pageParam = 1 }) => {
      return api.getHistory(pageParam as number, PAGE_SIZE);
    },
    getNextPageParam: (lastPage) => {
      // Return next page number if there are more pages
      if (lastPage.page < lastPage.total_pages) {
        return lastPage.page + 1;
      }
      return undefined;
    },
    initialPageParam: 1,
    staleTime: 10 * 60 * 1000, // 10 minutes
    gcTime: 30 * 60 * 1000, // 30 minutes
  });
}
