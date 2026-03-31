import React, { createContext, useContext, useEffect, useState } from "react";
import { revenueCat } from "@/services/revenuecat";
import { api } from "@/services/api";
import { PurchasesPackage } from "react-native-purchases";

interface SubscriptionContextType {
  isPremium: boolean;
  isLoading: boolean;
  purchasePackage: (pkg: PurchasesPackage) => Promise<void>;
  restorePurchases: () => Promise<void>;
  refreshStatus: () => Promise<void>;
}

const SubscriptionContext = createContext<SubscriptionContextType | undefined>(
  undefined,
);

export function SubscriptionProvider({ children }: { children: React.ReactNode }) {
  const [isPremium, setIsPremium] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const refreshStatus = async () => {
    try {
      setIsLoading(true);
      const status = await revenueCat.isPremium();
      setIsPremium(status);
      
      // Also sync with backend if needed
      if (status && revenueCat.isInitialized()) {
        const info = await revenueCat.getCustomerInfo();
        const expirationDate = await revenueCat.getPremiumExpirationDate();
        
        if (info) {
          await api.updateSubscription({
            user_id: info.originalAppUserId,
            is_premium: true,
            expires_at: expirationDate?.toISOString(),
          });
        }
      }
    } catch (error) {
      console.error("[SubscriptionContext] Error refreshing status:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const init = async () => {
      await revenueCat.initialize();
      await refreshStatus();
    };
    init();
  }, []);

  const purchasePackage = async (pkg: PurchasesPackage) => {
    await revenueCat.purchasePackage(pkg);
    await refreshStatus();
  };

  const restorePurchases = async () => {
    await revenueCat.restorePurchases();
    await refreshStatus();
  };

  return (
    <SubscriptionContext.Provider
      value={{
        isPremium,
        isLoading,
        purchasePackage,
        restorePurchases,
        refreshStatus,
      }}
    >
      {children}
    </SubscriptionContext.Provider>
  );
}

export function useSubscription() {
  const context = useContext(SubscriptionContext);
  if (context === undefined) {
    throw new Error("useSubscription must be used within a SubscriptionProvider");
  }
  return context;
}
