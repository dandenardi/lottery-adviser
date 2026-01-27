/**
 * Storage Service
 * Handles AsyncStorage operations for device ID, cache, and user preferences
 */

import AsyncStorage from "@react-native-async-storage/async-storage";
import * as Device from "expo-device";

// ============================================================================
// Storage Keys
// ============================================================================

const STORAGE_KEYS = {
  DEVICE_ID: "@lottery_adviser:device_id",
  USER_PREFERENCES: "@lottery_adviser:preferences",
  CACHE_PREFIX: "@lottery_adviser:cache:",
} as const;

// ============================================================================
// Types
// ============================================================================

export interface UserPreferences {
  theme?: "light" | "dark" | "auto";
  notifications_enabled?: boolean;
}

// ============================================================================
// Device ID Management
// ============================================================================

/**
 * Generate a unique device ID
 */
function generateDeviceId(): string {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2, 15);
  const deviceName = Device.deviceName || "unknown";
  return `${deviceName}_${timestamp}_${random}`;
}

/**
 * Get or create device ID
 * This ID is used for rate limiting and user identification
 */
export async function getDeviceId(): Promise<string> {
  try {
    let deviceId = await AsyncStorage.getItem(STORAGE_KEYS.DEVICE_ID);

    if (!deviceId) {
      deviceId = generateDeviceId();
      await AsyncStorage.setItem(STORAGE_KEYS.DEVICE_ID, deviceId);
      console.log("[Storage] Generated new device ID:", deviceId);
    }

    return deviceId;
  } catch (error) {
    console.error("[Storage] Error getting device ID:", error);
    // Fallback to in-memory ID if storage fails
    return generateDeviceId();
  }
}

// ============================================================================
// User Preferences
// ============================================================================

/**
 * Get user preferences
 */
export async function getUserPreferences(): Promise<UserPreferences> {
  try {
    const prefsJson = await AsyncStorage.getItem(STORAGE_KEYS.USER_PREFERENCES);
    return prefsJson ? JSON.parse(prefsJson) : {};
  } catch (error) {
    console.error("[Storage] Error getting preferences:", error);
    return {};
  }
}

/**
 * Save user preferences
 */
export async function saveUserPreferences(
  preferences: UserPreferences,
): Promise<void> {
  try {
    await AsyncStorage.setItem(
      STORAGE_KEYS.USER_PREFERENCES,
      JSON.stringify(preferences),
    );
  } catch (error) {
    console.error("[Storage] Error saving preferences:", error);
  }
}

/**
 * Update specific preference
 */
export async function updatePreference<K extends keyof UserPreferences>(
  key: K,
  value: UserPreferences[K],
): Promise<void> {
  try {
    const prefs = await getUserPreferences();
    prefs[key] = value;
    await saveUserPreferences(prefs);
  } catch (error) {
    console.error("[Storage] Error updating preference:", error);
  }
}

// ============================================================================
// Cache Management
// ============================================================================

interface CacheEntry<T> {
  data: T;
  timestamp: number;
  expiresAt: number;
}

/**
 * Save data to cache with expiration
 */
export async function setCache<T>(
  key: string,
  data: T,
  ttlSeconds: number = 300, // 5 minutes default
): Promise<void> {
  try {
    const now = Date.now();
    const entry: CacheEntry<T> = {
      data,
      timestamp: now,
      expiresAt: now + ttlSeconds * 1000,
    };

    await AsyncStorage.setItem(
      `${STORAGE_KEYS.CACHE_PREFIX}${key}`,
      JSON.stringify(entry),
    );
  } catch (error) {
    console.error("[Storage] Error setting cache:", error);
  }
}

/**
 * Get data from cache if not expired
 */
export async function getCache<T>(key: string): Promise<T | null> {
  try {
    const entryJson = await AsyncStorage.getItem(
      `${STORAGE_KEYS.CACHE_PREFIX}${key}`,
    );

    if (!entryJson) {
      return null;
    }

    const entry: CacheEntry<T> = JSON.parse(entryJson);
    const now = Date.now();

    if (now > entry.expiresAt) {
      // Cache expired, remove it
      await AsyncStorage.removeItem(`${STORAGE_KEYS.CACHE_PREFIX}${key}`);
      return null;
    }

    return entry.data;
  } catch (error) {
    console.error("[Storage] Error getting cache:", error);
    return null;
  }
}

/**
 * Clear specific cache entry
 */
export async function clearCache(key: string): Promise<void> {
  try {
    await AsyncStorage.removeItem(`${STORAGE_KEYS.CACHE_PREFIX}${key}`);
  } catch (error) {
    console.error("[Storage] Error clearing cache:", error);
  }
}

/**
 * Clear all cache entries
 */
export async function clearAllCache(): Promise<void> {
  try {
    const keys = await AsyncStorage.getAllKeys();
    const cacheKeys = keys.filter((key) =>
      key.startsWith(STORAGE_KEYS.CACHE_PREFIX),
    );
    await AsyncStorage.multiRemove(cacheKeys);
  } catch (error) {
    console.error("[Storage] Error clearing all cache:", error);
  }
}

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Clear all app data (for debugging/logout)
 */
export async function clearAllData(): Promise<void> {
  try {
    await AsyncStorage.clear();
    console.log("[Storage] All data cleared");
  } catch (error) {
    console.error("[Storage] Error clearing all data:", error);
  }
}

/**
 * Get storage info (for debugging)
 */
export async function getStorageInfo(): Promise<{
  deviceId: string;
  preferences: UserPreferences;
  cacheKeys: string[];
}> {
  try {
    const deviceId = await getDeviceId();
    const preferences = await getUserPreferences();
    const allKeys = await AsyncStorage.getAllKeys();
    const cacheKeys = allKeys.filter((key) =>
      key.startsWith(STORAGE_KEYS.CACHE_PREFIX),
    );

    return {
      deviceId,
      preferences,
      cacheKeys,
    };
  } catch (error) {
    console.error("[Storage] Error getting storage info:", error);
    return {
      deviceId: "unknown",
      preferences: {},
      cacheKeys: [],
    };
  }
}
