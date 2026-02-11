"""
Update and Analyze Pipeline - Main orchestration logic.

This module provides the main pipeline function that orchestrates
loading data, updating it, and running analysis.
"""

from typing import Dict
import asyncio

from app.services.statistics_service import LotteryStatisticsService
from app.services.data.lotofacil_fetcher import get_fetcher
from app.core.database import SessionLocal


async def run_pipeline() -> Dict[str, any]:
    """
    Execute the main lottery analysis pipeline.
    
    This function orchestrates the entire workflow:
    1. Fetch latest results from API and update database
    2. Run statistical analysis from database
    3. Return results
    
    Returns:
        dict: Statistical analysis results from the LotteryStatisticsService.
    """
    db = SessionLocal()
    try:
        # Step 1: Fetch and update with latest results
        print("Checking for new lottery results...")
        fetcher = get_fetcher()
        update_result = await fetcher.update_database(db)
        
        if update_result.get("success"):
            if update_result.get("contests_added", 0) > 0:
                print(f"Update successful: {update_result.get('message')}")
            else:
                print("Database is already up to date")
        else:
            print(f"Warning: Could not update database: {update_result.get('error')}")
            print("Proceeding with existing data...")

        # Step 2: Run statistical analysis
        print("\nComputing statistics from database...")
        statistics_service = LotteryStatisticsService(db)
        stats = statistics_service.compute_statistics()
        print("Statistics computed successfully")

        return stats
    finally:
        db.close()
