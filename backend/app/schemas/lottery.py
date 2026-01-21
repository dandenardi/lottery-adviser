"""
Pydantic schemas for API request/response validation.
"""

from datetime import date, datetime
from typing import List, Dict, Any, Optional
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class StrategyType(str, Enum):
    """Available strategy types for number generation."""
    BALANCED = "balanced"
    HOT_NUMBERS = "hot_numbers"
    COLD_NUMBERS = "cold_numbers"
    WEIGHTED_RANDOM = "weighted_random"
    RECENT_PATTERNS = "recent_patterns"


# Lottery Result Schemas

class LotteryResultBase(BaseModel):
    """Base schema for lottery results."""
    contest_number: int = Field(..., description="Contest number", ge=1)
    draw_date: date = Field(..., description="Draw date")
    numbers: List[int] = Field(..., description="Drawn numbers", min_length=15, max_length=15)
    
    @field_validator('numbers')
    @classmethod
    def validate_numbers(cls, v):
        """Validate that numbers are in valid range and unique."""
        if len(v) != len(set(v)):
            raise ValueError("Numbers must be unique")
        if not all(1 <= num <= 25 for num in v):
            raise ValueError("Numbers must be between 1 and 25")
        return sorted(v)


class LotteryResultResponse(LotteryResultBase):
    """Response schema for lottery results."""
    id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}


class LatestResultResponse(BaseModel):
    """Response schema for latest result."""
    contest: int
    date: str
    numbers: List[int]


# Statistics Schemas

class NumberFrequency(BaseModel):
    """Schema for number frequency data."""
    number: int
    frequency: int


class EvenOddDistribution(BaseModel):
    """Schema for even/odd distribution."""
    even: int
    odd: int
    even_percentage: float
    odd_percentage: float


class StatisticsResponse(BaseModel):
    """Response schema for statistics."""
    total_contests: int
    date_range: Dict[str, str]
    most_common_numbers: List[NumberFrequency]
    least_common_numbers: List[NumberFrequency]
    average_sum: float
    even_odd_distribution: EvenOddDistribution
    number_range_distribution: Dict[str, int]
    total_numbers_analyzed: int


# Suggestion Schemas

class SuggestionMetadata(BaseModel):
    """Metadata about a suggestion."""
    hot_numbers_count: int
    cold_numbers_count: int
    even_count: int
    odd_count: int
    sum: int
    quality_score: float
    range_distribution: Dict[str, int]


class SuggestionResponse(BaseModel):
    """Response schema for a single suggestion."""
    numbers: List[int]
    strategy: str
    metadata: SuggestionMetadata
    generated_at: datetime


class GenerateSuggestionsRequest(BaseModel):
    """Request schema for generating suggestions."""
    strategy: StrategyType = Field(default=StrategyType.BALANCED, description="Strategy to use")
    count: int = Field(default=1, ge=1, le=10, description="Number of suggestions to generate")
    user_id: str = Field(..., description="User/device ID for rate limiting")


class GenerateSuggestionsResponse(BaseModel):
    """Response schema for generated suggestions."""
    suggestions: List[SuggestionResponse]
    remaining_today: Optional[int] = Field(None, description="Remaining suggestions for free users")
    is_premium: bool = Field(default=False, description="Whether user is premium")


# User/Subscription Schemas

class UserSubscriptionStatus(BaseModel):
    """Response schema for user subscription status."""
    user_id: str
    is_premium: bool
    expires_at: Optional[datetime] = None


class UpdateSubscriptionRequest(BaseModel):
    """Request schema for updating subscription status."""
    user_id: str
    is_premium: bool
    subscription_id: Optional[str] = None
    expires_at: Optional[datetime] = None


# History Schemas

class HistoryResponse(BaseModel):
    """Response schema for history endpoint."""
    results: List[LotteryResultResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# Health Check

class HealthCheckResponse(BaseModel):
    """Response schema for health check."""
    status: str
    version: str
    database: str
    timestamp: datetime
