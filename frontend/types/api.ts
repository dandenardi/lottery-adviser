/**
 * TypeScript types for Lottery Adviser API
 * Based on backend Pydantic schemas
 */

// ============================================================================
// Enums
// ============================================================================

export enum StrategyType {
  BALANCED = "balanced",
  HOT_NUMBERS = "hot_numbers",
  COLD_NUMBERS = "cold_numbers",
  WEIGHTED_RANDOM = "weighted_random",
  RECENT_PATTERNS = "recent_patterns",
}

// ============================================================================
// Lottery Results
// ============================================================================

export interface LotteryResult {
  id: number;
  contest_number: number;
  draw_date: string; // ISO date string
  numbers: number[];
  created_at: string; // ISO datetime string
}

export interface LatestResult {
  contest: number;
  date: string;
  numbers: number[];
}

// ============================================================================
// Statistics
// ============================================================================

export interface NumberFrequency {
  number: number;
  frequency: number;
}

export interface EvenOddDistribution {
  even: number;
  odd: number;
  even_percentage: number;
  odd_percentage: number;
}

export interface Statistics {
  total_contests: number;
  date_range: {
    start: string;
    end: string;
  };
  most_common_numbers: NumberFrequency[];
  least_common_numbers: NumberFrequency[];
  average_sum: number;
  even_odd_distribution: EvenOddDistribution;
  number_range_distribution: Record<string, number>;
  total_numbers_analyzed: number;
}

// ============================================================================
// Suggestions
// ============================================================================

export interface SuggestionMetadata {
  hot_numbers_count: number;
  cold_numbers_count: number;
  even_count: number;
  odd_count: number;
  sum: number;
  quality_score: number;
  range_distribution: Record<string, number>;
}

export interface Suggestion {
  numbers: number[];
  strategy: string;
  metadata: SuggestionMetadata;
  generated_at: string; // ISO datetime string
}

export interface GenerateSuggestionsRequest {
  strategy?: StrategyType;
  count?: number; // 1-10
  user_id: string;
}

export interface GenerateSuggestionsResponse {
  suggestions: Suggestion[];
  remaining_today?: number;
  is_premium: boolean;
}

// ============================================================================
// User/Subscription
// ============================================================================

export interface UserSubscriptionStatus {
  user_id: string;
  is_premium: boolean;
  expires_at?: string; // ISO datetime string
}

export interface UpdateSubscriptionRequest {
  user_id: string;
  is_premium: boolean;
  subscription_id?: string;
  expires_at?: string; // ISO datetime string
}

// ============================================================================
// History
// ============================================================================

export interface HistoryResponse {
  results: LotteryResult[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// ============================================================================
// Health Check
// ============================================================================

export interface HealthCheckResponse {
  status: string;
  version: string;
  database: string;
  timestamp: string; // ISO datetime string
}

// ============================================================================
// API Error Response
// ============================================================================

export interface APIError {
  detail: string;
  status_code?: number;
}
