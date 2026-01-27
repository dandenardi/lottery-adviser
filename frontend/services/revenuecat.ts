/**
 * RevenueCat Service
 * Handles in-app purchases and subscription management
 */

import Purchases, {
  CustomerInfo,
  PurchasesOfferings,
  PurchasesPackage,
  LOG_LEVEL,
} from "react-native-purchases";
import { Platform } from "react-native";
import { getDeviceId } from "./storage";

// ============================================================================
// Configuration
// ============================================================================

const REVENUECAT_API_KEY_ANDROID =
  process.env.EXPO_PUBLIC_REVENUECAT_API_KEY_ANDROID || "";
const REVENUECAT_API_KEY_IOS =
  process.env.EXPO_PUBLIC_REVENUECAT_API_KEY_IOS || "";

// Entitlement identifier (configured in RevenueCat dashboard)
const PREMIUM_ENTITLEMENT = "premium";

// ============================================================================
// RevenueCat Service Class
// ============================================================================

class RevenueCatService {
  private initialized = false;

  /**
   * Initialize RevenueCat SDK
   * Should be called once at app startup
   */
  async initialize(): Promise<void> {
    if (this.initialized) {
      console.log("[RevenueCat] Already initialized");
      return;
    }

    try {
      // Get device ID for user identification
      const deviceId = await getDeviceId();

      // Configure SDK based on platform
      const apiKey =
        Platform.OS === "android"
          ? REVENUECAT_API_KEY_ANDROID
          : REVENUECAT_API_KEY_IOS;

      if (!apiKey) {
        console.warn("[RevenueCat] API key not configured");
        return;
      }

      // Configure RevenueCat
      Purchases.configure({
        apiKey,
        appUserID: deviceId,
      });

      // Set log level for debugging
      if (__DEV__) {
        Purchases.setLogLevel(LOG_LEVEL.DEBUG);
      }

      this.initialized = true;
      console.log("[RevenueCat] Initialized successfully");
    } catch (error) {
      console.error("[RevenueCat] Initialization error:", error);
      throw error;
    }
  }

  /**
   * Get available offerings (subscription plans)
   */
  async getOfferings(): Promise<PurchasesOfferings> {
    try {
      const offerings = await Purchases.getOfferings();

      if (__DEV__) {
        console.log("[RevenueCat] Available offerings:", offerings);
      }

      return offerings;
    } catch (error) {
      console.error("[RevenueCat] Error getting offerings:", error);
      throw error;
    }
  }

  /**
   * Purchase a package
   */
  async purchasePackage(pkg: PurchasesPackage): Promise<CustomerInfo> {
    try {
      const { customerInfo } = await Purchases.purchasePackage(pkg);

      if (__DEV__) {
        console.log("[RevenueCat] Purchase successful:", customerInfo);
      }

      return customerInfo;
    } catch (error: any) {
      // Handle user cancellation
      if (error.userCancelled) {
        console.log("[RevenueCat] Purchase cancelled by user");
      } else {
        console.error("[RevenueCat] Purchase error:", error);
      }
      throw error;
    }
  }

  /**
   * Restore previous purchases
   */
  async restorePurchases(): Promise<CustomerInfo> {
    try {
      const customerInfo = await Purchases.restorePurchases();

      if (__DEV__) {
        console.log("[RevenueCat] Purchases restored:", customerInfo);
      }

      return customerInfo;
    } catch (error) {
      console.error("[RevenueCat] Restore error:", error);
      throw error;
    }
  }

  /**
   * Get customer info (subscription status)
   */
  async getCustomerInfo(): Promise<CustomerInfo> {
    try {
      const customerInfo = await Purchases.getCustomerInfo();
      return customerInfo;
    } catch (error) {
      console.error("[RevenueCat] Error getting customer info:", error);
      throw error;
    }
  }

  /**
   * Check if user has premium subscription
   */
  async isPremium(): Promise<boolean> {
    try {
      const customerInfo = await this.getCustomerInfo();
      const hasPremium =
        customerInfo.entitlements.active[PREMIUM_ENTITLEMENT] !== undefined;

      if (__DEV__) {
        console.log("[RevenueCat] Premium status:", hasPremium);
      }

      return hasPremium;
    } catch (error) {
      console.error("[RevenueCat] Error checking premium status:", error);
      return false;
    }
  }

  /**
   * Get premium expiration date
   */
  async getPremiumExpirationDate(): Promise<Date | null> {
    try {
      const customerInfo = await this.getCustomerInfo();
      const entitlement = customerInfo.entitlements.active[PREMIUM_ENTITLEMENT];

      if (entitlement && entitlement.expirationDate) {
        return new Date(entitlement.expirationDate);
      }

      return null;
    } catch (error) {
      console.error("[RevenueCat] Error getting expiration date:", error);
      return null;
    }
  }

  /**
   * Logout current user
   */
  async logout(): Promise<void> {
    try {
      await Purchases.logOut();
      this.initialized = false;
      console.log("[RevenueCat] User logged out");
    } catch (error) {
      console.error("[RevenueCat] Logout error:", error);
      throw error;
    }
  }
}

// ============================================================================
// Export singleton instance
// ============================================================================

export const revenueCat = new RevenueCatService();
export default revenueCat;
