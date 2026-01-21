"""Quick test of the strategy generator."""

from pathlib import Path
from app.analysis.strategy_generator import StrategyType, LotteryStrategyGenerator
from app.storage.history_repository import LotteryHistoryRepository
from app.analysis.statistics_service import LotteryStatisticsService

# Load data
print("Loading Lotofácil data...")
repo = LotteryHistoryRepository(Path('data/raw/loto_facil_asloterias_ate_concurso_3576_sorteio.xlsx'))
history = repo.load_history()
print(f"✅ Loaded {len(history)} contests")

# Compute statistics
print("\nComputing statistics...")
stats_service = LotteryStatisticsService()
stats = stats_service.compute_statistics(history)
print(f"✅ Analyzed {stats['total_numbers_analyzed']} numbers")

# Generate suggestion
print("\nGenerating balanced suggestion...")
generator = LotteryStrategyGenerator(stats, history)
suggestions = generator.generate_suggestions(StrategyType.BALANCED, 1)

# Display
suggestion = suggestions[0]
print(f"\n🎲 Suggestion: {sorted(suggestion['numbers'])}")
print(f"\n📊 Metadata:")
for key, value in suggestion['metadata'].items():
    print(f"   {key}: {value}")
