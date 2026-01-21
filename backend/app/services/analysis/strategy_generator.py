"""
Lottery Strategy Generator - Generates number suggestions using various strategies.

This module provides the LotteryStrategyGenerator class for generating
intelligent lottery number suggestions based on historical data analysis.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Set
import random

import pandas as pd

from app.core.config import settings


class StrategyType(Enum):
    """Available strategy types for number generation."""
    
    BALANCED = "balanced"
    HOT_NUMBERS = "hot_numbers"
    COLD_NUMBERS = "cold_numbers"
    WEIGHTED_RANDOM = "weighted_random"
    RECENT_PATTERNS = "recent_patterns"


class LotteryStrategyGenerator:
    """
    Service for generating lottery number suggestions using various strategies.
    
    This class implements multiple heuristic strategies for generating
    lottery number combinations based on statistical analysis of historical data.
    """

    def __init__(self, statistics: Dict[str, any], history: pd.DataFrame):
        """
        Initialize the strategy generator.
        
        Args:
            statistics: Statistical analysis from LotteryStatisticsService
            history: Historical lottery data DataFrame
        """
        self.statistics = statistics
        self.history = history
        self.number_frequencies = statistics.get("number_frequencies", {})
        
    def generate_suggestions(
        self, 
        strategy: StrategyType = StrategyType.BALANCED,
        count: int = 1
    ) -> List[Dict[str, any]]:
        """
        Generate lottery number suggestions using the specified strategy.
        
        Args:
            strategy: The strategy type to use for generation
            count: Number of suggestions to generate
            
        Returns:
            List of suggestion dictionaries, each containing:
                - strategy: Strategy name used
                - numbers: List of suggested numbers (sorted)
                - metadata: Additional information about the suggestion
                - generated_at: Timestamp of generation
        """
        suggestions = []
        
        for _ in range(count):
            if strategy == StrategyType.BALANCED:
                numbers = self._balanced_strategy()
            elif strategy == StrategyType.HOT_NUMBERS:
                numbers = self._hot_numbers_strategy()
            elif strategy == StrategyType.COLD_NUMBERS:
                numbers = self._cold_numbers_strategy()
            elif strategy == StrategyType.WEIGHTED_RANDOM:
                numbers = self._weighted_random_strategy()
            elif strategy == StrategyType.RECENT_PATTERNS:
                numbers = self._recent_patterns_strategy()
            else:
                raise ValueError(f"Unknown strategy: {strategy}")
            
            # Create suggestion with metadata
            suggestion = {
                "strategy": strategy.value,
                "numbers": sorted(numbers),
                "metadata": self._calculate_metadata(numbers),
                "generated_at": datetime.now().isoformat(),
            }
            
            suggestions.append(suggestion)
        
        return suggestions
    
    def _balanced_strategy(self) -> List[int]:
        """
        Balanced strategy: Mix of hot and cold numbers with even distribution.
        
        Returns:
            List of suggested numbers
        """
        numbers: Set[int] = set()
        
        # Get hot and cold numbers
        sorted_freq = sorted(self.number_frequencies.items(), key=lambda x: x[1], reverse=True)
        hot_numbers = [int(num) for num, _ in sorted_freq[:10]]
        cold_numbers = [int(num) for num, _ in sorted_freq[-10:]]
        
        # Select mix: 40% hot, 30% cold, 30% random
        hot_count = int(settings.numbers_per_game * 0.4)
        cold_count = int(settings.numbers_per_game * 0.3)
        random_count = settings.numbers_per_game - hot_count - cold_count
        
        # Add hot numbers
        numbers.update(random.sample(hot_numbers, min(hot_count, len(hot_numbers))))
        
        # Add cold numbers
        numbers.update(random.sample(cold_numbers, min(cold_count, len(cold_numbers))))
        
        # Fill remaining with random numbers
        all_numbers = set(range(settings.lottery_min_number, settings.lottery_max_number + 1))
        available = all_numbers - numbers
        numbers.update(random.sample(list(available), min(random_count, len(available))))
        
        # Ensure we have exactly NUMBERS_PER_GAME numbers
        while len(numbers) < settings.numbers_per_game:
            available = all_numbers - numbers
            if available:
                numbers.add(random.choice(list(available)))
        
        return list(numbers)
    
    def _hot_numbers_strategy(self) -> List[int]:
        """
        Hot numbers strategy: Prioritize most frequently drawn numbers.
        
        Returns:
            List of suggested numbers
        """
        sorted_freq = sorted(self.number_frequencies.items(), key=lambda x: x[1], reverse=True)
        
        # Take top numbers with some randomization
        top_numbers = [int(num) for num, _ in sorted_freq[:settings.numbers_per_game * 2]]
        
        return random.sample(top_numbers, settings.numbers_per_game)
    
    def _cold_numbers_strategy(self) -> List[int]:
        """
        Cold numbers strategy: Prioritize least frequently drawn numbers.
        
        Returns:
            List of suggested numbers
        """
        sorted_freq = sorted(self.number_frequencies.items(), key=lambda x: x[1])
        
        # Take bottom numbers with some randomization
        bottom_numbers = [int(num) for num, _ in sorted_freq[:settings.numbers_per_game * 2]]
        
        return random.sample(bottom_numbers, settings.numbers_per_game)
    
    def _weighted_random_strategy(self) -> List[int]:
        """
        Weighted random strategy: Random selection weighted by historical frequency.
        
        Returns:
            List of suggested numbers
        """
        numbers_list = list(self.number_frequencies.keys())
        weights = list(self.number_frequencies.values())
        
        # Normalize weights
        total_weight = sum(weights)
        normalized_weights = [w / total_weight for w in weights]
        
        # Sample without replacement
        selected = []
        available_indices = list(range(len(numbers_list)))
        available_weights = normalized_weights.copy()
        
        for _ in range(settings.numbers_per_game):
            if not available_indices:
                break
                
            # Renormalize weights
            weight_sum = sum(available_weights)
            if weight_sum > 0:
                probs = [w / weight_sum for w in available_weights]
            else:
                probs = [1 / len(available_weights)] * len(available_weights)
            
            # Choose index position from available indices
            chosen_position = random.choices(range(len(available_indices)), weights=probs, k=1)[0]
            chosen_idx = available_indices[chosen_position]
            selected.append(int(numbers_list[chosen_idx]))
            
            # Remove chosen index
            available_indices.pop(chosen_position)
            available_weights.pop(chosen_position)
        
        return selected
    
    def _recent_patterns_strategy(self) -> List[int]:
        """
        Recent patterns strategy: Analyze recent draws for trends.
        
        Returns:
            List of suggested numbers
        """
        # Get recent draws
        recent_history = self.history.tail(settings.recent_draws_window)
        
        # Identify number columns (handles both 'bola_' and 'bola ' formats)
        number_columns = [col for col in recent_history.columns if str(col).startswith("bola")]
        if not number_columns:
            number_columns = [
                col for col in recent_history.columns 
                if col not in ["concurso", "data"] and pd.api.types.is_numeric_dtype(recent_history[col])
            ]
        
        # Count frequencies in recent draws
        recent_numbers = []
        for col in number_columns:
            recent_numbers.extend(recent_history[col].dropna().tolist())
        
        recent_freq = pd.Series(recent_numbers).value_counts().to_dict()
        
        # Prioritize numbers that appeared in recent draws
        if recent_freq:
            sorted_recent = sorted(recent_freq.items(), key=lambda x: x[1], reverse=True)
            trending_numbers = [int(num) for num, _ in sorted_recent[:settings.numbers_per_game * 2]]
            
            # Mix trending with some random
            selected = set(random.sample(trending_numbers, min(int(settings.numbers_per_game * 0.7), len(trending_numbers))))
            
            # Fill remaining with random
            all_numbers = set(range(settings.lottery_min_number, settings.lottery_max_number + 1))
            available = all_numbers - selected
            selected.update(random.sample(list(available), settings.numbers_per_game - len(selected)))
            
            return list(selected)
        else:
            # Fallback to balanced strategy
            return self._balanced_strategy()
    
    def _calculate_metadata(self, numbers: List[int]) -> Dict[str, any]:
        """
        Calculate metadata about a suggestion.
        
        Args:
            numbers: List of suggested numbers
            
        Returns:
            Dictionary with metadata including distribution statistics
        """
        # Count even/odd
        even_count = sum(1 for n in numbers if n % 2 == 0)
        odd_count = len(numbers) - even_count
        
        # Categorize as hot/cold
        sorted_freq = sorted(self.number_frequencies.items(), key=lambda x: x[1], reverse=True)
        hot_threshold = len(sorted_freq) // 3
        cold_threshold = 2 * len(sorted_freq) // 3
        
        hot_numbers = {int(num) for num, _ in sorted_freq[:hot_threshold]}
        cold_numbers = {int(num) for num, _ in sorted_freq[cold_threshold:]}
        
        hot_count = sum(1 for n in numbers if n in hot_numbers)
        cold_count = sum(1 for n in numbers if n in cold_numbers)
        
        # Range distribution (divide into 3 ranges for Lotofácil)
        range_size = (settings.lottery_max_number - settings.lottery_min_number + 1) // 3
        range_dist = {
            f"{settings.lottery_min_number}-{settings.lottery_min_number + range_size - 1}": 0,
            f"{settings.lottery_min_number + range_size}-{settings.lottery_min_number + 2*range_size - 1}": 0,
            f"{settings.lottery_min_number + 2*range_size}-{settings.lottery_max_number}": 0,
        }
        
        for num in numbers:
            if num < settings.lottery_min_number + range_size:
                range_dist[f"{settings.lottery_min_number}-{settings.lottery_min_number + range_size - 1}"] += 1
            elif num < settings.lottery_min_number + 2*range_size:
                range_dist[f"{settings.lottery_min_number + range_size}-{settings.lottery_min_number + 2*range_size - 1}"] += 1
            else:
                range_dist[f"{settings.lottery_min_number + 2*range_size}-{settings.lottery_max_number}"] += 1
        
        # Calculate quality score (0-1)
        # Based on balance of even/odd, hot/cold, and range distribution
        even_odd_balance = 1 - abs(even_count - odd_count) / len(numbers)
        hot_cold_balance = 1 - abs(hot_count - cold_count) / len(numbers) if (hot_count + cold_count) > 0 else 0.5
        range_balance = 1 - max(range_dist.values()) / len(numbers)
        
        quality_score = (even_odd_balance + hot_cold_balance + range_balance) / 3
        
        return {
            "hot_numbers_count": hot_count,
            "cold_numbers_count": cold_count,
            "even_count": even_count,
            "odd_count": odd_count,
            "range_distribution": range_dist,
            "sum": sum(numbers),
            "quality_score": round(quality_score, 2),
        }
