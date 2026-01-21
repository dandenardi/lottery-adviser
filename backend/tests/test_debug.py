"""Test strategies one by one to find the error."""

from pathlib import Path
from app.analysis.strategy_generator import LotteryStrategyGenerator, StrategyType
from app.storage.history_repository import LotteryHistoryRepository
from app.analysis.statistics_service import LotteryStatisticsService
import traceback

# Load data
print("Loading data...")
repo = LotteryHistoryRepository(Path('data/raw/loto_facil_asloterias_ate_concurso_3576_sorteio.xlsx'))
history = repo.load_history()
print(f"Loaded {len(history)} contests")

# Compute statistics
print("\nComputing statistics...")
stats_service = LotteryStatisticsService()
stats = stats_service.compute_statistics(history)
print(f"Analyzed {stats['total_numbers_analyzed']} numbers")

# Test each strategy
generator = LotteryStrategyGenerator(stats, history)

strategies = [
    (StrategyType.BALANCED, "Balanced"),
    (StrategyType.HOT_NUMBERS, "Hot Numbers"),
    (StrategyType.COLD_NUMBERS, "Cold Numbers"),
    (StrategyType.WEIGHTED_RANDOM, "Weighted Random"),
    (StrategyType.RECENT_PATTERNS, "Recent Patterns"),
]

for strategy_type, strategy_name in strategies:
    print(f"\nTesting {strategy_name}...")
    try:
        suggestion = generator.generate_suggestions(strategy_type, 1)[0]
        print(f"  ✅ Success: {len(suggestion['numbers'])} numbers generated")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        traceback.print_exc()
