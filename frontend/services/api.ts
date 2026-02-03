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
    return process.env.EXPO_PUBLIC_API_BASE_URL || "http://localhost:5000";
  }

  // For mobile (Android/iOS) - use network IP from env
  // This works for both Expo Go and emulators when backend binds to 0.0.0.0
  return (
    process.env.EXPO_PUBLIC_API_BASE_URL_MOBILE || "http://192.168.0.107:5000"
  );
};

const API_BASE_URL = getApiBaseUrl();
const API_PREFIX = "/api/v1";

// Debug: Log the API URL being used
if (__DEV__) {
  console.log(`[API Config] Using base URL: ${API_BASE_URL}${API_PREFIX}`);
  console.log(`[API Config] Platform: ${Platform.OS}`);
}

// ============================================================================
// API Client Class
// ============================================================================

class LotteryAPI {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_BASE_URL}${API_PREFIX}`,
      timeout: 10000,
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
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.detail || "An error occurred";
      return new Error(message);
    } else if (error.request) {
      // Request made but no response received
      return new Error("Network error. Please check your connection.");
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
