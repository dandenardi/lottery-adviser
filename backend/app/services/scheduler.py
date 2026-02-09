"""Scheduler service for automated lottery data updates."""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.services.data.lotofacil_fetcher import get_fetcher

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = AsyncIOScheduler()


async def update_lottery_data():
    """
    Scheduled task to update lottery data from Caixa API.
    This runs automatically based on the configured schedule.
    """
    logger.info("Starting scheduled lottery data update...")
    
    db: Session = SessionLocal()
    try:
        fetcher = get_fetcher()
        result = await fetcher.update_database(db)
        
        if result.get("success"):
            logger.info(
                f"✅ Lottery data update completed: {result.get('message')} "
                f"(Latest contest: {result.get('latest_contest')})"
            )
        else:
            logger.error(f"❌ Lottery data update failed: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"Error in scheduled update: {e}")
    finally:
        db.close()


def setup_scheduler():
    """
    Configure and set up scheduled tasks.
    Called during application startup.
    """
    if not settings.scheduler_enabled:
        logger.info("Scheduler is disabled in settings")
        return
    
    # Schedule daily lottery data update
    scheduler.add_job(
        update_lottery_data,
        CronTrigger(
            hour=settings.scheduler_update_hour,
            minute=settings.scheduler_update_minute
        ),
        id="update_lottery_data",
        name="Update lottery results from Caixa API",
        replace_existing=True
    )
    
    logger.info(
        f"📅 Scheduled lottery data update at "
        f"{settings.scheduler_update_hour:02d}:{settings.scheduler_update_minute:02d} daily"
    )


def start_scheduler():
    """Start the scheduler."""
    setup_scheduler()
    scheduler.start()
    logger.info("✅ Scheduler started")


def shutdown_scheduler():
    """Shutdown the scheduler gracefully."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shut down")
