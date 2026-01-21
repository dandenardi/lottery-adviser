"""
Subscription management service.
"""

from datetime import datetime
from sqlalchemy.orm import Session

from app.models.lottery import UserSubscription
from app.schemas.lottery import UpdateSubscriptionRequest, UserSubscriptionStatus


class SubscriptionService:
    """Service for managing user subscriptions."""
    
    def __init__(self, db: Session):
        """Initialize the service with database session."""
        self.db = db
    
    def get_subscription(self, user_id: str) -> UserSubscriptionStatus:
        """
        Get user subscription status.
        
        Args:
            user_id: User/device ID
            
        Returns:
            UserSubscriptionStatus
        """
        subscription = self.db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id
        ).first()
        
        if not subscription:
            # Create default free subscription
            subscription = UserSubscription(
                user_id=user_id,
                is_premium=False
            )
            self.db.add(subscription)
            self.db.commit()
            self.db.refresh(subscription)
        
        return UserSubscriptionStatus(
            user_id=subscription.user_id,
            is_premium=subscription.is_premium,
            expires_at=subscription.expires_at
        )
    
    def update_subscription(self, request: UpdateSubscriptionRequest) -> UserSubscriptionStatus:
        """
        Update user subscription status.
        
        This is typically called by RevenueCat webhook or manual admin action.
        
        Args:
            request: Update subscription request
            
        Returns:
            Updated UserSubscriptionStatus
        """
        subscription = self.db.query(UserSubscription).filter(
            UserSubscription.user_id == request.user_id
        ).first()
        
        if not subscription:
            subscription = UserSubscription(user_id=request.user_id)
            self.db.add(subscription)
        
        subscription.is_premium = request.is_premium
        subscription.subscription_id = request.subscription_id
        subscription.expires_at = request.expires_at
        subscription.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(subscription)
        
        return UserSubscriptionStatus(
            user_id=subscription.user_id,
            is_premium=subscription.is_premium,
            expires_at=subscription.expires_at
        )
    
    def cancel_subscription(self, user_id: str) -> UserSubscriptionStatus:
        """
        Cancel user subscription.
        
        Args:
            user_id: User/device ID
            
        Returns:
            Updated UserSubscriptionStatus
        """
        subscription = self.db.query(UserSubscription).filter(
            UserSubscription.user_id == user_id
        ).first()
        
        if subscription:
            subscription.is_premium = False
            subscription.expires_at = None
            subscription.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(subscription)
        
        return UserSubscriptionStatus(
            user_id=user_id,
            is_premium=False,
            expires_at=None
        )
