/**
 * API Client for Lottery Adviser Backend
 * Handles all HTTP communication with the FastAPI backend
 */

import axios, { AxiosInstance, AxiosError } from "axios";
import {
  LatestResult,
  Statistics,
  GenerateSuggestionsRequest,
  GenerateSuggestionsResponse,
  HistoryResponse,
  LotteryResult,
  UserSubscriptionStatus,
  UpdateSubscriptionRequest,
  HealthCheckResponse,
  APIError,
} from "@/types/api";

// ============================================================================
// Configuration
// ============================================================================

import { Platform } from "react-native";

// Automatically select the correct API URL based on platform
const getApiBaseUrl = (): string => {
  if (Platform.OS === "web") {
    return (
      process.env.EXPO_PUBLIC_API_BASE_URL ||
      "https://lottery-adviser-api.onrender.com"
    );
  }

  // For mobile (Android/iOS)
  // 1. Try mobile-specific env var (usually for dev/local)
  // 2. Try generic base URL (usually for prod)
  // 3. Fallback to production Render URL (SAFEST for APKs)
  return (
    process.env.EXPO_PUBLIC_API_BASE_URL_MOBILE ||
    process.env.EXPO_PUBLIC_API_BASE_URL ||
    "https://lottery-adviser-api.onrender.com"
  );
};

const API_BASE_URL = getApiBaseUrl();
const API_PREFIX = "/api/v1";

// CRITICAL: Always log the API URL being used to help debug production APKs
console.log(`[API Config] Using base URL: ${API_BASE_URL}${API_PREFIX}`);

if (__DEV__) {
  console.log(`[API Config] Platform: ${Platform.OS}`);
  console.log(`[API Config] Environment: Development`);
} else {
  console.log(`[API Config] Environment: Production/Release`);
}

// ============================================================================
// API Client Class
// ============================================================================

class LotteryAPI {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_BASE_URL}${API_PREFIX}`,
      timeout: 60000, // 60s para lidar com cold start do Render (free tier)
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Request interceptor for logging in dev mode
    this.client.interceptors.request.use(
      (config) => {
        if (__DEV__) {
          console.log(
            `[API Request] ${config.method?.toUpperCase()} ${config.url}`,
          );
        }
        return config;
      },
      (error) => {
        if (__DEV__) {
          console.error("[API Request Error]", error);
        }
        return Promise.reject(error);
      },
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => {
        if (__DEV__) {
          console.log(`[API Response] ${response.config.url}`, response.status);
        }
        return response;
      },
      (error: AxiosError<APIError>) => {
        if (__DEV__) {
          console.error("[API Error]", error.response?.data || error.message);
        }
        return Promise.reject(this.handleError(error));
      },
    );
  }

  /**
   * Handle API errors and transform them into a consistent format
   */
  private handleError(error: AxiosError<APIError>): Error {
    const url = error.config?.url || "unknown";
    const fullUrl = `${this.client.defaults.baseURL}${url}`;
    
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.detail || "An error occurred";
      return new Error(`${message} (Status: ${error.response.status})`);
    } else if (error.request) {
      // Request made but no response received
      return new Error(`Network error. Failed to reach: ${fullUrl}. Please check your connection and ensure the server is up.`);
    } else {
      // Something else happened
      return new Error(error.message || "An unexpected error occurred");
    }
  }

  // ==========================================================================
  // Results Endpoints
  // ==========================================================================

  /**
   * Get the latest lottery result
   */
  async getLatestResult(): Promise<LatestResult> {
    const response = await this.client.get<LatestResult>("/results/latest");
    return response.data;
  }

  /**
   * Get result by contest number
   */
  async getResultByContest(contestNumber: number): Promise<LotteryResult> {
    const response = await this.client.get<LotteryResult>(
      `/results/${contestNumber}`,
    );
    return response.data;
  }

  /**
   * Get paginated history of results
   */
  async getHistory(
    page: number = 1,
    pageSize: number = 20,
  ): Promise<HistoryResponse> {
    const response = await this.client.get<HistoryResponse>("/history", {
      params: { page, page_size: pageSize },
    });
    return response.data;
  }

  // ==========================================================================
  // Statistics Endpoints
  // ==========================================================================

  /**
   * Get lottery statistics
   */
  async getStatistics(): Promise<Statistics> {
    const response = await this.client.get<Statistics>("/statistics");
    return response.data;
  }

  // ==========================================================================
  // Suggestions Endpoints
  // ==========================================================================

  /**
   * Generate lottery number suggestions
   */
  async generateSuggestions(
    request: GenerateSuggestionsRequest,
  ): Promise<GenerateSuggestionsResponse> {
    const response = await this.client.post<GenerateSuggestionsResponse>(
      "/suggestions",
      request,
    );
    return response.data;
  }

  // ==========================================================================
  // Subscription Endpoints
  // ==========================================================================

  /**
   * Get user subscription status
   */
  async getSubscriptionStatus(userId: string): Promise<UserSubscriptionStatus> {
    const response = await this.client.get<UserSubscriptionStatus>(
      `/subscriptions/${userId}`,
    );
    return response.data;
  }

  /**
   * Update user subscription status
   */
  async updateSubscription(
    request: UpdateSubscriptionRequest,
  ): Promise<UserSubscriptionStatus> {
    const response = await this.client.post<UserSubscriptionStatus>(
      "/subscriptions",
      request,
    );
    return response.data;
  }

  // ==========================================================================
  // Health Check
  // ==========================================================================

  /**
   * Check API health status
   */
  async healthCheck(): Promise<HealthCheckResponse> {
    const response = await this.client.get<HealthCheckResponse>("/health");
    return response.data;
  }
}

// ============================================================================
// Export singleton instance
// ============================================================================

export const api = new LotteryAPI();
export default api;
