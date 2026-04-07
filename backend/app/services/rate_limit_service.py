"""
Rate Limiting Service for free tier users.
"""

from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from app.models.lottery import UserSuggestionUsage, UserSubscription
from app.core.config import settings


class RateLimitService:
    """Service for managing rate limits on suggestions."""
    
    def __init__(self, db: Session):
        """Initialize the service with database session."""
        self.db = db
    
    def check_and_increment(self, user_id: str) -> tuple[bool, int]:
        """
        Check if user can generate suggestions and increment counter.
        
        Args:
            user_id: User/device ID
            
        Returns:
            Tuple of (can_generate, remaining_count)
        """
        # Check if user is premium
        if self.is_premium(user_id):
            return True, -1  # -1 indicates unlimited
        
        # Check today's usage for free users
        today = date.today()
        usage = self.db.query(UserSuggestionUsage).filter(
            UserSuggestionUsage.user_id == user_id,
            UserSuggestionUsage.date == today
        ).first()
        
        if not usage:
            # Create new usage record
            usage = UserSuggestionUsage(
                user_id=user_id,
                date=today,
                suggestions_count=1,
                rewarded_suggestions_count=0,
                is_premium=False
            )
            self.db.add(usage)
            self.db.commit()
            remaining = settings.rate_limit_suggestions_per_day - 1
            return True, remaining
        
        # Check if basic limit reached
        if usage.suggestions_count < settings.rate_limit_suggestions_per_day:
            # Still have basic suggestions
            usage.suggestions_count += 1
            usage.updated_at = datetime.utcnow()
            self.db.commit()
            remaining = settings.rate_limit_suggestions_per_day - usage.suggestions_count
            return True, remaining
        
        # Basic limit reached, check rewarded suggestions
        if usage.rewarded_suggestions_count > 0:
            usage.rewarded_suggestions_count -= 1
            # We also increment suggestions_count to track total? 
            # No, let's keep them separate to avoid confusion.
            usage.suggestions_count += 1 
            usage.updated_at = datetime.utcnow()
            self.db.commit()
            return True, usage.rewarded_suggestions_count
            
        return False, 0

    def add_reward(self, user_id: str, count: int = 1) -> int:
        """
        Add rewarded suggestions to a user for today.
        
        Args:
            user_id: User/device ID
            count: Number of suggestions to add
            
        Returns:
            New total of rewarded suggestions
        """
        today = date.today()
        usage = self.db.query(UserSuggestionUsage).filter(
            UserSuggestionUsage.user_id == user_id,
            UserSuggestionUsage.date == today
        ).first()
        
        if not usage:
            usage = UserSuggestionUsage(
                user_id=user_id,
                date=today,
                suggestions_count=0,
                rewarded_suggestions_count=count,
                is_premium=False
            )
            self.db.add(usage)
        else:
            usage.rewarded_suggestions_count += count
            usage.updated_at = datetime.utcnow()
            
        self.db.commit()
        return usage.rewarded_suggestions_count

    def get_rewarded_remaining(self, user_id: str) -> int:
        """Get remaining rewarded suggestions."""
        today = date.today()
        usage = self.db.query(UserSuggestionUsage).filter(
            UserSuggestionUsage.user_id == user_id,
            UserSuggestionUsage.date == today
        ).first()
        
        if not usage:
            return 0
        return usage.rewarded_suggestions_count
    
    def get_remaining_count(self, user_id: str) -> int:
        """
        Get remaining suggestions count for today.
        
        Args:
            user_id: User/device ID
            
        Returns:
            Remaining count (-1 for premium/unlimited)
        """
        # Check if premium
        subscription = self.db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id
        ).first()
        
        if subscription and subscription.is_premium:
            if subscription.expires_at is None or subscription.expires_at > datetime.utcnow():
                return -1  # Unlimited
        
        # Check today's usage
        today = date.today()
        usage = self.db.query(UserSuggestionUsage).filter(
            UserSuggestionUsage.user_id == user_id,
            UserSuggestionUsage.date == today
        ).first()
        
    def get_remaining_count(self, user_id: str) -> int:
        """
        Get remaining suggestions count for today.
        
        Args:
            user_id: User/device ID
            
        Returns:
            Remaining count (-1 for premium/unlimited)
        """
        if self.is_premium(user_id):
            return -1  # Unlimited
        
        # Check today's usage
        today = date.today()
        usage = self.db.query(UserSuggestionUsage).filter(
            UserSuggestionUsage.user_id == user_id,
            UserSuggestionUsage.date == today
        ).first()
        
        if not usage:
            return settings.rate_limit_suggestions_per_day
        
        # Total remaining = (basic remaining) + rewarded
        basic_remaining = max(0, settings.rate_limit_suggestions_per_day - usage.suggestions_count)
        return basic_remaining + usage.rewarded_suggestions_count
    
    def is_premium(self, user_id: str) -> bool:
        """
        Check if user has active premium subscription.
        
        Args:
            user_id: User/device ID
            
        Returns:
            True if premium, False otherwise
        """
        subscription = self.db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id
        ).first()
        
        if not subscription or not subscription.is_premium:
            return False
        
        # Check expiration
        if subscription.expires_at and subscription.expires_at <= datetime.utcnow():
            # Subscription expired, update status
            subscription.is_premium = False
            self.db.commit()
            return False
        
        return True
