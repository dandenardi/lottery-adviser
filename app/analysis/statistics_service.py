"""
Lottery Statistics Service - Computes statistical analysis of lottery data.

This module provides the LotteryStatisticsService class for analyzing
historical lottery data and computing various statistics.
"""

from typing import Dict, List

import pandas as pd


class LotteryStatisticsService:
    """
    Service for computing statistical analysis on lottery data.
    
    This class provides pure statistical analysis without any LLM logic.
    It computes frequencies, aggregates, and other statistical measures.
    """

    def compute_statistics(self, history: pd.DataFrame) -> Dict[str, any]:
        """
        Compute comprehensive statistics from the lottery history.
        
        Args:
            history: DataFrame containing historical lottery data.
                    Expected to have 'concurso', 'data', and number columns.
        
        Returns:
            dict: A structured dictionary containing:
                - total_contests: Total number of contests
                - date_range: First and last draw dates
                - number_frequencies: Frequency of each number drawn
                - most_common_numbers: Top 10 most frequently drawn numbers
                - least_common_numbers: Top 10 least frequently drawn numbers
                - average_sum: Average sum of drawn numbers
                - even_odd_distribution: Distribution of even vs odd numbers
                - number_range_distribution: Distribution across number ranges
        """
        if history.empty:
            return {
                "error": "No data available for analysis",
                "total_contests": 0,
            }

        # Identify number columns (assuming they start with 'bola_' or are numeric)
        number_columns = [col for col in history.columns if col.startswith("bola_")]
        
        # If no 'bola_' columns, try to find numeric columns (excluding 'concurso')
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

        # Number range distribution (assuming lottery numbers are 1-60)
        # Adjust ranges based on your specific lottery
        ranges = {
            "1-15": 0,
            "16-30": 0,
            "31-45": 0,
            "46-60": 0,
        }
        
        for num in all_numbers:
            if 1 <= num <= 15:
                ranges["1-15"] += 1
            elif 16 <= num <= 30:
                ranges["16-30"] += 1
            elif 31 <= num <= 45:
                ranges["31-45"] += 1
            elif 46 <= num <= 60:
                ranges["46-60"] += 1

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
