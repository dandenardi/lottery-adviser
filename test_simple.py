"""Test all strategies - simple output."""

from pathlib import Path
from app.analysis.strategy_generator import LotteryStrategyGenerator, StrategyType
from app.storage.history_repository import LotteryHistoryRepository
from app.analysis.statistics_service import LotteryStatisticsService

print("=" * 70)
print("  LOTOFACIL - TESTE DE TODAS AS ESTRATEGIAS")
print("=" * 70)

# Load data
print("\nCarregando dados historicos...")
repo = LotteryHistoryRepository(Path('data/raw/loto_facil_asloterias_ate_concurso_3576_sorteio.xlsx'))
history = repo.load_history()
print(f"OK - {len(history)} concursos carregados")

# Compute statistics
print("\nCalculando estatisticas...")
stats_service = LotteryStatisticsService()
stats = stats_service.compute_statistics(history)
print(f"OK - {stats['total_numbers_analyzed']} numeros analisados")

# Test all strategies
generator = LotteryStrategyGenerator(stats, history)

strategies = [
    (StrategyType.BALANCED, "Balanceada"),
    (StrategyType.HOT_NUMBERS, "Hot Numbers"),
    (StrategyType.COLD_NUMBERS, "Cold Numbers"),
    (StrategyType.WEIGHTED_RANDOM, "Aleatoria Ponderada"),
    (StrategyType.RECENT_PATTERNS, "Padroes Recentes"),
]

print("\n" + "=" * 70)
print("  TESTANDO TODAS AS ESTRATEGIAS")
print("=" * 70)

for strategy_type, strategy_name in strategies:
    print(f"\n{'-' * 70}")
    print(f"  {strategy_name}")
    print(f"{'-' * 70}")
    
    suggestion = generator.generate_suggestions(strategy_type, 1)[0]
    numbers = suggestion['numbers']
    metadata = suggestion['metadata']
    
    # Format numbers
    numbers_str = " - ".join(f"{num:02d}" for num in numbers)
    print(f"\n  Numeros: {numbers_str}")
    
    print(f"\n  Estatisticas:")
    print(f"     - Numeros quentes: {metadata['hot_numbers_count']}")
    print(f"     - Numeros frios: {metadata['cold_numbers_count']}")
    print(f"     - Pares: {metadata['even_count']} | Impares: {metadata['odd_count']}")
    print(f"     - Soma total: {metadata['sum']}")
    print(f"     - Score de qualidade: {metadata['quality_score']:.2f}")
    
    print(f"\n  Distribuicao por faixa:")
    for range_name, count in metadata['range_distribution'].items():
        print(f"     - {range_name}: {count} numeros")

print(f"\n{'=' * 70}")
print("  TESTE CONCLUIDO COM SUCESSO!")
print(f"{'=' * 70}\n")
