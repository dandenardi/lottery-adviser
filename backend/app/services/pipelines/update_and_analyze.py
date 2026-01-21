"""
Update and Analyze Pipeline - Main orchestration logic.

This module provides the main pipeline function that orchestrates
loading data, updating it (in future), and running analysis.
"""

from typing import Dict

from app.services.analysis import LotteryStatisticsService
from app.services.collectors import LotteryCollector
from app.services.storage import LotteryHistoryRepository


def run_pipeline() -> Dict[str, any]:
    """
    Execute the main lottery analysis pipeline.
    
    This function orchestrates the entire workflow:
    1. Load historical data from storage
    2. (Future) Fetch latest result and update dataset if needed
    3. Run statistical analysis
    4. Return results
    
    Returns:
        dict: Statistical analysis results from the LotteryStatisticsService.
    
    Raises:
        FileNotFoundError: If the historical data file is not found.
        ValueError: If the data is invalid or empty.
    """
    # Initialize components
    repository = LotteryHistoryRepository()
    statistics_service = LotteryStatisticsService()
    collector = LotteryCollector()  # Not used yet, but initialized for future use

    # Step 1: Load historical data
    print("Loading historical lottery data...")
    history = repository.load_history()
    print(f"✓ Loaded {len(history)} contests from history")

    # Step 2: (Future) Fetch and update with latest result
    # This will be implemented in a future milestone
    # try:
    #     latest_result = collector.fetch_latest_result()
    #     if not repository.has_concurso(latest_result["concurso"]):
    #         repository.append_result(latest_result)
    #         print(f"✓ Added new contest: {latest_result['concurso']}")
    #         history = repository.load_history()  # Reload with new data
    # except NotImplementedError:
    #     print("⚠ Skipping update - scraping not implemented yet")

    # Step 3: Run statistical analysis
    print("\nComputing statistics...")
    stats = statistics_service.compute_statistics(history)
    print("✓ Statistics computed successfully")

    return stats
