"""Test all strategies automatically."""

from pathlib import Path
from app.analysis.strategy_generator import LotteryStrategyGenerator, StrategyType
from app.storage.history_repository import LotteryHistoryRepository
from app.analysis.statistics_service import LotteryStatisticsService

print("=" * 70)
print("  🎰 LOTOFÁCIL - TESTE DE TODAS AS ESTRATÉGIAS 🎰")
print("=" * 70)

# Load data
print("\n📂 Carregando dados históricos...")
repo = LotteryHistoryRepository(Path('data/raw/loto_facil_asloterias_ate_concurso_3576_sorteio.xlsx'))
history = repo.load_history()
print(f"✅ {len(history)} concursos carregados")

# Compute statistics
print("\n📊 Calculando estatísticas...")
stats_service = LotteryStatisticsService()
stats = stats_service.compute_statistics(history)
print(f"✅ {stats['total_numbers_analyzed']} números analisados")

# Test all strategies
generator = LotteryStrategyGenerator(stats, history)

strategies = [
    (StrategyType.BALANCED, "🎯 Balanceada"),
    (StrategyType.HOT_NUMBERS, "🔥 Hot Numbers"),
    (StrategyType.COLD_NUMBERS, "❄️  Cold Numbers"),
    (StrategyType.WEIGHTED_RANDOM, "🎲 Aleatória Ponderada"),
    (StrategyType.RECENT_PATTERNS, "📈 Padrões Recentes"),
]

print("\n" + "=" * 70)
print("  TESTANDO TODAS AS ESTRATÉGIAS")
print("=" * 70)

for strategy_type, strategy_name in strategies:
    print(f"\n{'─' * 70}")
    print(f"  {strategy_name}")
    print(f"{'─' * 70}")
    
    suggestion = generator.generate_suggestions(strategy_type, 1)[0]
    numbers = suggestion['numbers']
    metadata = suggestion['metadata']
    
    # Format numbers
    numbers_str = " - ".join(f"{num:02d}" for num in numbers)
    print(f"\n  Números: {numbers_str}")
    
    print(f"\n  📊 Estatísticas:")
    print(f"     • Números quentes: {metadata['hot_numbers_count']}")
    print(f"     • Números frios: {metadata['cold_numbers_count']}")
    print(f"     • Pares: {metadata['even_count']} | Ímpares: {metadata['odd_count']}")
    print(f"     • Soma total: {metadata['sum']}")
    print(f"     • Score de qualidade: {metadata['quality_score']:.2f}")
    
    print(f"\n  📍 Distribuição por faixa:")
    for range_name, count in metadata['range_distribution'].items():
        print(f"     • {range_name}: {count} números")

print(f"\n{'=' * 70}")
print("  ✨ TESTE CONCLUÍDO COM SUCESSO! ✨")
print(f"{'=' * 70}\n")
