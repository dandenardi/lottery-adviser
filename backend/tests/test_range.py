"""Verify numbers are in correct range (1-25)."""

from pathlib import Path
from app.analysis.strategy_generator import LotteryStrategyGenerator, StrategyType
from app.storage.history_repository import LotteryHistoryRepository
from app.analysis.statistics_service import LotteryStatisticsService

# Load data
repo = LotteryHistoryRepository(Path('data/raw/loto_facil_asloterias_ate_concurso_3576_sorteio.xlsx'))
history = repo.load_history()

# Compute statistics
stats_service = LotteryStatisticsService()
stats = stats_service.compute_statistics(history)

# Generate suggestions
generator = LotteryStrategyGenerator(stats, history)

print("Testing all strategies for correct number range (1-25):")
print()

strategies = [
    (StrategyType.BALANCED, "Balanced"),
    (StrategyType.HOT_NUMBERS, "Hot Numbers"),
    (StrategyType.COLD_NUMBERS, "Cold Numbers"),
    (StrategyType.WEIGHTED_RANDOM, "Weighted Random"),
    (StrategyType.RECENT_PATTERNS, "Recent Patterns"),
]

all_valid = True

for strategy_type, strategy_name in strategies:
    suggestion = generator.generate_suggestions(strategy_type, 1)[0]
    numbers = suggestion['numbers']
    
    # Check range
    min_num = min(numbers)
    max_num = max(numbers)
    in_range = all(1 <= n <= 25 for n in numbers)
    
    status = "OK" if in_range else "FAIL"
    print(f"[{status}] {strategy_name:20} - Min: {min_num:2d}, Max: {max_num:2d}, Count: {len(numbers)}")
    print(f"     Numbers: {sorted(numbers)}")
    
    if not in_range:
        all_valid = False
        print(f"     WARNING: Numbers outside range 1-25!")
    print()

print("-" * 60)
if all_valid:
    print("SUCCESS: All strategies generate valid Lotofacil numbers (1-25)!")
else:
    print("ERROR: Some strategies generate invalid numbers!")
