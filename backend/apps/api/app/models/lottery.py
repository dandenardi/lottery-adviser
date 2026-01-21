"""
Database models for lottery data.
"""

from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Date, Float
from sqlalchemy.dialects.postgresql import ARRAY

from app.core.database import Base


class LotteryResult(Base):
    """Model for storing lottery results."""
    
    __tablename__ = "lottery_results"
    
    id = Column(Integer, primary_key=True, index=True)
    contest_number = Column(Integer, unique=True, index=True, nullable=False)
    draw_date = Column(Date, nullable=False)
    numbers = Column(ARRAY(Integer), nullable=False)  # Array of drawn numbers
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<LotteryResult(contest={self.contest_number}, date={self.draw_date})>"


class UserSuggestionUsage(Base):
    """Model for tracking user suggestion usage (rate limiting)."""
    
    __tablename__ = "user_suggestion_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)  # Device ID or user ID
    date = Column(Date, nullable=False, index=True)
    suggestions_count = Column(Integer, default=0)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserSuggestionUsage(user={self.user_id}, date={self.date}, count={self.suggestions_count})>"


class UserSubscription(Base):
    """Model for storing user subscription status."""
    
    __tablename__ = "user_subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    is_premium = Column(Boolean, default=False)
    subscription_id = Column(String, nullable=True)  # RevenueCat subscription ID
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserSubscription(user={self.user_id}, premium={self.is_premium})>"


class CachedStatistics(Base):
    """Model for caching computed statistics."""
    
    __tablename__ = "cached_statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String, unique=True, index=True, nullable=False)
    data = Column(JSON, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<CachedStatistics(key={self.cache_key})>"
