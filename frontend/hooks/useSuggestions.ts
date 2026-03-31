/**
 * React Query hook for generating lottery suggestions
 */

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/services/api";
import { getDeviceId } from "@/services/storage";
import type {
  GenerateSuggestionsRequest,
  GenerateSuggestionsResponse,
  AdRewardResponse,
  StrategyType,
} from "@/types/api";

interface GenerateSuggestionsParams {
  strategy?: StrategyType;
  count?: number;
}

export function useSuggestions() {
  const queryClient = useQueryClient();

  const mutation = useMutation<
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
      // Invalidate the premium status query to keep everything in sync
      queryClient.invalidateQueries({ queryKey: ["premium-status"] });
      
      if (__DEV__) {
        console.log("[useSuggestions] Generated suggestions:", data);
      }
    },
    onError: (error) => {
      console.error("[useSuggestions] Error:", error);
    },
  });

  const claimReward = useMutation<AdRewardResponse, Error, void>({
    mutationFn: async () => {
      const deviceId = await getDeviceId();
      return api.claimAdReward({ user_id: deviceId });
    },
    onSuccess: () => {
      // Refresh any data if needed
      if (__DEV__) {
        console.log("[useSuggestions] Reward claimed successfully");
      }
    },
  });

  return {
    ...mutation,
    claimReward,
  };
}
