"""
Subscription management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.lottery import UpdateSubscriptionRequest, UserSubscriptionStatus
from app.services.subscription_service import SubscriptionService

router = APIRouter(prefix="/api/v1/subscriptions", tags=["subscriptions"])


@router.get("/{user_id}", response_model=UserSubscriptionStatus)
async def get_subscription_status(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get user subscription status.
    
    Args:
        user_id: User/device ID
        
    Returns:
        User subscription status
    """
    service = SubscriptionService(db)
    return service.get_subscription(user_id)


@router.post("/update", response_model=UserSubscriptionStatus)
async def update_subscription(
    request: UpdateSubscriptionRequest,
    db: Session = Depends(get_db)
):
    """
    Update user subscription status.
    
    This endpoint is typically called by RevenueCat webhook.
    In production, this should be protected with webhook signature validation.
    
    Args:
        request: Subscription update request
        
    Returns:
        Updated subscription status
    """
    # TODO: Add RevenueCat webhook signature validation
    # For now, this is a simple update endpoint
    
    service = SubscriptionService(db)
    return service.update_subscription(request)


@router.delete("/{user_id}", response_model=UserSubscriptionStatus)
async def cancel_subscription(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Cancel user subscription.
    
    Args:
        user_id: User/device ID
        
    Returns:
        Updated subscription status
    """
    service = SubscriptionService(db)
    return service.cancel_subscription(user_id)
