"""
Lottery Statistics Service - Adapted from existing codebase.

This service computes statistical analysis of lottery data.
"""

from typing import Dict, List
import pandas as pd
from sqlalchemy.orm import Session

from app.models.lottery import LotteryResult
from app.core.config import settings


class LotteryStatisticsService:
    """
    Service for computing statistical analysis on lottery data.
    
    Adapted from the original app/analysis/statistics_service.py
    """
    
    def __init__(self, db: Session):
        """Initialize the service with database session."""
        self.db = db
    
    def get_history_dataframe(self) -> pd.DataFrame:
        """
        Load lottery history from database into DataFrame.
        
        Returns:
            DataFrame with lottery history
        """
        results = self.db.query(LotteryResult).order_by(LotteryResult.contest_number).all()
        
        if not results:
            return pd.DataFrame()
        
        # Convert to DataFrame format similar to original
        data = []
        for result in results:
            row = {
                'concurso': result.contest_number,
                'data': result.draw_date,
            }
            # Add number columns
            for i, num in enumerate(result.numbers, start=1):
                row[f'bola_{i}'] = num
            data.append(row)
        
        return pd.DataFrame(data)
    
    def compute_statistics(self) -> Dict[str, any]:
        """
        Compute comprehensive statistics from the lottery history.
        
        Returns:
            dict: A structured dictionary containing statistics
        """
        history = self.get_history_dataframe()
        
        if history.empty:
            return {
                "error": "No data available for analysis",
                "total_contests": 0,
            }

        # Identify number columns
        number_columns = [col for col in history.columns if str(col).startswith("bola")]
        
        if not number_columns:
            number_columns = [
                col
                for col in history.columns
                if col not in ["concurso", "data"] and pd.api.types.is_numeric_dtype(history[col])
            ]

        # Basic statistics
        total_contests = len(history)
        
        # Date range
        if "data" in history.columns:
            date_range = {
                "first_draw": str(history["data"].min()),
                "last_draw": str(history["data"].max()),
            }
        else:
            date_range = {"first_draw": "N/A", "last_draw": "N/A"}

        # Number frequency analysis
        all_numbers = []
        for col in number_columns:
            all_numbers.extend(history[col].dropna().tolist())

        number_frequencies = pd.Series(all_numbers).value_counts().to_dict()
        
        # Most and least common numbers
        sorted_frequencies = sorted(number_frequencies.items(), key=lambda x: x[1], reverse=True)
        most_common = [
            {"number": int(num), "frequency": int(freq)} 
            for num, freq in sorted_frequencies[:10]
        ]
        least_common = [
            {"number": int(num), "frequency": int(freq)} 
            for num, freq in sorted_frequencies[-10:]
        ]

        # Average sum of drawn numbers per contest
        sums = history[number_columns].sum(axis=1)
        average_sum = float(sums.mean())
        
        # Even/Odd distribution
        even_count = sum(1 for num in all_numbers if num % 2 == 0)
        odd_count = len(all_numbers) - even_count
        even_odd_distribution = {
            "even": even_count,
            "odd": odd_count,
            "even_percentage": round(even_count / len(all_numbers) * 100, 2),
            "odd_percentage": round(odd_count / len(all_numbers) * 100, 2),
        }

        # Number range distribution
        range_size = (settings.lottery_max_number - settings.lottery_min_number + 1) // 3
        ranges = {
            f"{settings.lottery_min_number}-{settings.lottery_min_number + range_size - 1}": 0,
            f"{settings.lottery_min_number + range_size}-{settings.lottery_min_number + 2*range_size - 1}": 0,
            f"{settings.lottery_min_number + 2*range_size}-{settings.lottery_max_number}": 0,
        }
        
        for num in all_numbers:
            if settings.lottery_min_number <= num < settings.lottery_min_number + range_size:
                ranges[f"{settings.lottery_min_number}-{settings.lottery_min_number + range_size - 1}"] += 1
            elif settings.lottery_min_number + range_size <= num < settings.lottery_min_number + 2*range_size:
                ranges[f"{settings.lottery_min_number + range_size}-{settings.lottery_min_number + 2*range_size - 1}"] += 1
            else:
                ranges[f"{settings.lottery_min_number + 2*range_size}-{settings.lottery_max_number}"] += 1

        return {
            "total_contests": total_contests,
            "date_range": date_range,
            "number_frequencies": number_frequencies,
            "most_common_numbers": most_common,
            "least_common_numbers": least_common,
            "average_sum": average_sum,
            "even_odd_distribution": even_odd_distribution,
            "number_range_distribution": ranges,
            "total_numbers_analyzed": len(all_numbers),
        }
