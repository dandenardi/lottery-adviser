/**
 * React Query hook for generating lottery suggestions
 */

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/services/api";
import { getDeviceId } from "@/services/storage";
import type {
  GenerateSuggestionsRequest,
  GenerateSuggestionsResponse,
  StrategyType,
} from "@/types/api";

interface GenerateSuggestionsParams {
  strategy?: StrategyType;
  count?: number;
}

export function useSuggestions() {
  const queryClient = useQueryClient();

  return useMutation<
    GenerateSuggestionsResponse,
    Error,
    GenerateSuggestionsParams
  >({
    mutationFn: async (params) => {
      const deviceId = await getDeviceId();

      const request: GenerateSuggestionsRequest = {
        user_id: deviceId,
        strategy: params.strategy,
        count: params.count,
      };

      return api.generateSuggestions(request);
    },
    onSuccess: (data) => {
      // Optionally invalidate related queries
      if (__DEV__) {
        console.log("[useSuggestions] Generated suggestions:", data);
      }
    },
    onError: (error) => {
      console.error("[useSuggestions] Error:", error);
    },
  });
}
