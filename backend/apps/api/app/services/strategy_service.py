"""
Lottery Strategy Generator - Adapted from existing codebase.

This service generates number suggestions using various strategies.
"""

from datetime import datetime
from typing import Dict, List
import random
import pandas as pd
from sqlalchemy.orm import Session

from app.services.statistics_service import LotteryStatisticsService
from app.schemas.lottery import StrategyType
from app.core.config import settings


class LotteryStrategyGenerator:
    """
    Service for generating lottery number suggestions using various strategies.
    
    Adapted from the original app/analysis/strategy_generator.py
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
    ) -> List[Dict]:
        """
        Generate lottery number suggestions using the specified strategy.
        
        Args:
            strategy: The strategy type to use for generation
            count: Number of suggestions to generate
            
        Returns:
            List of suggestion dictionaries
        """
        suggestions = []
        
        for _ in range(count):
            # Generate numbers based on strategy
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
                numbers = self._balanced_strategy()
            
            # Calculate metadata
            metadata = self._calculate_metadata(numbers)
            
            suggestions.append({
                "numbers": numbers,
                "strategy": strategy.value,
                "metadata": metadata,
                "generated_at": datetime.utcnow(),
            })
        
        return suggestions
    
    def _balanced_strategy(self) -> List[int]:
        """Balanced strategy: Mix of hot and cold numbers with even distribution."""
        hot_numbers = [item["number"] for item in self.statistics["most_common_numbers"][:10]]
        cold_numbers = [item["number"] for item in self.statistics["least_common_numbers"][:10]]
        
        # Select 5 hot, 5 cold, 5 random
        selected = set()
        selected.update(random.sample(hot_numbers, min(5, len(hot_numbers))))
        selected.update(random.sample(cold_numbers, min(5, len(cold_numbers))))
        
        # Fill remaining with random numbers
        all_numbers = set(range(settings.lottery_min_number, settings.lottery_max_number + 1))
        remaining = list(all_numbers - selected)
        selected.update(random.sample(remaining, settings.numbers_per_game - len(selected)))
        
        return sorted(list(selected))[:settings.numbers_per_game]
    
    def _hot_numbers_strategy(self) -> List[int]:
        """Hot numbers strategy: Prioritize most frequently drawn numbers."""
        hot_numbers = [item["number"] for item in self.statistics["most_common_numbers"]]
        
        # Take top numbers and add some randomness
        selected = set(hot_numbers[:12])
        selected = random.sample(list(selected), settings.numbers_per_game)
        
        return sorted(selected)
    
    def _cold_numbers_strategy(self) -> List[int]:
        """Cold numbers strategy: Prioritize least frequently drawn numbers."""
        cold_numbers = [item["number"] for item in self.statistics["least_common_numbers"]]
        
        # Take least common numbers and add some randomness
        selected = set(cold_numbers[:12])
        selected = random.sample(list(selected), settings.numbers_per_game)
        
        return sorted(selected)
    
    def _weighted_random_strategy(self) -> List[int]:
        """Weighted random strategy: Random selection weighted by historical frequency."""
        numbers = list(self.number_frequencies.keys())
        weights = list(self.number_frequencies.values())
        
        # Normalize weights
        total_weight = sum(weights)
        probabilities = [w / total_weight for w in weights]
        
        # Select numbers with weighted probability
        selected = set()
        while len(selected) < settings.numbers_per_game:
            num = random.choices(numbers, weights=probabilities, k=1)[0]
            selected.add(num)
        
        return sorted(list(selected))
    
    def _recent_patterns_strategy(self) -> List[int]:
        """Recent patterns strategy: Analyze recent draws for trends."""
        if self.history.empty:
            return self._balanced_strategy()
        
        # Get recent draws
        recent_window = min(10, len(self.history))
        recent_draws = self.history.tail(recent_window)
        
        # Identify number columns
        number_columns = [col for col in recent_draws.columns if str(col).startswith("bola")]
        
        # Count frequencies in recent draws
        recent_numbers = []
        for col in number_columns:
            recent_numbers.extend(recent_draws[col].dropna().tolist())
        
        recent_freq = pd.Series(recent_numbers).value_counts()
        
        # Mix recent hot numbers with some random
        recent_hot = recent_freq.head(10).index.tolist()
        selected = set(random.sample(recent_hot, min(10, len(recent_hot))))
        
        # Fill remaining
        all_numbers = set(range(settings.lottery_min_number, settings.lottery_max_number + 1))
        remaining = list(all_numbers - selected)
        selected.update(random.sample(remaining, settings.numbers_per_game - len(selected)))
        
        return sorted(list(selected))[:settings.numbers_per_game]
    
    def _calculate_metadata(self, numbers: List[int]) -> Dict:
        """Calculate metadata about a suggestion."""
        hot_numbers = set(item["number"] for item in self.statistics["most_common_numbers"][:10])
        cold_numbers = set(item["number"] for item in self.statistics["least_common_numbers"][:10])
        
        hot_count = len([n for n in numbers if n in hot_numbers])
        cold_count = len([n for n in numbers if n in cold_numbers])
        even_count = len([n for n in numbers if n % 2 == 0])
        odd_count = len(numbers) - even_count
        
        # Range distribution
        range_size = (settings.lottery_max_number - settings.lottery_min_number + 1) // 3
        range_dist = {
            f"{settings.lottery_min_number}-{settings.lottery_min_number + range_size - 1}": 0,
            f"{settings.lottery_min_number + range_size}-{settings.lottery_min_number + 2*range_size - 1}": 0,
            f"{settings.lottery_min_number + 2*range_size}-{settings.lottery_max_number}": 0,
        }
        
        for num in numbers:
            if settings.lottery_min_number <= num < settings.lottery_min_number + range_size:
                range_dist[f"{settings.lottery_min_number}-{settings.lottery_min_number + range_size - 1}"] += 1
            elif settings.lottery_min_number + range_size <= num < settings.lottery_min_number + 2*range_size:
                range_dist[f"{settings.lottery_min_number + range_size}-{settings.lottery_min_number + 2*range_size - 1}"] += 1
            else:
                range_dist[f"{settings.lottery_min_number + 2*range_size}-{settings.lottery_max_number}"] += 1
        
        # Quality score (simple heuristic)
        balance_score = 1.0 - abs(even_count - odd_count) / len(numbers)
        diversity_score = (hot_count + cold_count) / len(numbers)
        quality_score = (balance_score + diversity_score) / 2
        
        return {
            "hot_numbers_count": hot_count,
            "cold_numbers_count": cold_count,
            "even_count": even_count,
            "odd_count": odd_count,
            "sum": sum(numbers),
            "quality_score": round(quality_score, 2),
            "range_distribution": range_dist,
        }
