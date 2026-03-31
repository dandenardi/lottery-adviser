"""
Subscription management endpoints.
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.schemas.lottery import UpdateSubscriptionRequest, UserSubscriptionStatus
from app.services.subscription_service import SubscriptionService

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


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
    # TODO: Add authentication for manual updates
    
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


@router.post("/webhook")
async def revenuecat_webhook(
    payload: dict,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Handle RevenueCat webhooks.
    """
    # Validate webhook secret if configured
    if settings.revenuecat_webhook_secret and authorization != settings.revenuecat_webhook_secret:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
        
    event = payload.get("event", {})
    event_type = event.get("type")
    app_user_id = event.get("app_user_id")
    
    if not app_user_id or not event_type:
        return {"status": "ignored"}
    
    service = SubscriptionService(db)
    
    if event_type in ["INITIAL_PURCHASE", "RENEWAL", "RESTORE"]:
        # Grant premium
        expiration_at_ms = event.get("expiration_at_ms")
        expires_at = None
        if expiration_at_ms:
            expires_at = datetime.fromtimestamp(expiration_at_ms / 1000.0)
            
        service.update_subscription(UpdateSubscriptionRequest(
            user_id=app_user_id,
            is_premium=True,
            subscription_id=event.get("product_id"),
            expires_at=expires_at
        ))
    elif event_type in ["EXPIRATION", "CANCELLATION", "BILLING_ERROR"]:
        # Revoke premium (or handle grace period)
        service.cancel_subscription(app_user_id)
        
    return {"status": "success"}
