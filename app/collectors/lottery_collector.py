"""
Lottery Collector - Responsible for fetching the latest lottery results.

This module provides the LotteryCollector class which will be responsible for
fetching lottery results from external sources (to be implemented in future milestones).
"""

from datetime import date
from typing import Dict, List


class LotteryCollector:
    """
    Collector for fetching lottery results.
    
    This class is responsible only for fetching the latest lottery result.
    The actual implementation will be added in future milestones when
    scraping logic is implemented.
    """

    def fetch_latest_result(self) -> Dict[str, any]:
        """
        Fetch the latest lottery result.
        
        Returns:
            dict: A dictionary containing:
                - concurso (int): The contest number
                - data (date): The date of the draw
                - numeros (list[int]): The drawn numbers
        
        Raises:
            NotImplementedError: This method is not yet implemented.
        
        Example:
            >>> collector = LotteryCollector()
            >>> result = collector.fetch_latest_result()
            >>> # Returns: {
            >>> #   "concurso": 2500,
            >>> #   "data": date(2024, 1, 15),
            >>> #   "numeros": [5, 12, 23, 34, 45, 56]
            >>> # }
        """
        raise NotImplementedError(
            "Lottery scraping is not implemented yet. "
            "This will be added in a future milestone."
        )
