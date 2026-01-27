/**
 * React Query hook for managing premium subscription status
 */

import { useQuery } from "@tanstack/react-query";
import { revenueCat } from "@/services/revenuecat";

export function usePremiumStatus() {
  return useQuery({
    queryKey: ["premium-status"],
    queryFn: async () => {
      const isPremium = await revenueCat.isPremium();
      const expirationDate = await revenueCat.getPremiumExpirationDate();

      return {
        isPremium,
        expirationDate,
      };
    },
    staleTime: 60 * 1000, // 1 minute
    gcTime: 5 * 60 * 1000, // 5 minutes
    retry: 1,
  });
}

/**
 * Hook to check if user has premium access
 * Returns a simple boolean for easy conditional rendering
 */
export function useIsPremium(): boolean {
  const { data } = usePremiumStatus();
  return data?.isPremium ?? false;
}
