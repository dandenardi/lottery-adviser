"""Quick CLI test - auto-generate one suggestion."""

from pathlib import Path
from app.analysis.statistics_service import LotteryStatisticsService
from app.analysis.strategy_generator import LotteryStrategyGenerator, StrategyType
from app.storage.history_repository import LotteryHistoryRepository
from app.config import LOTTERY_HISTORY_FILE

print("=" * 70)
print("  TESTE RAPIDO DO GERADOR DE SUGESTOES")
print("=" * 70)

# Load historical data
print(f"\nCarregando: {LOTTERY_HISTORY_FILE.name}")
repository = LotteryHistoryRepository(LOTTERY_HISTORY_FILE)
history = repository.load_history()
print(f"OK - {len(history)} concursos carregados")

# Compute statistics
stats_service = LotteryStatisticsService()
statistics = stats_service.compute_statistics(history)
print(f"OK - {statistics['total_numbers_analyzed']} numeros analisados")

# Generate suggestion
print("\nGerando sugestao balanceada...")
generator = LotteryStrategyGenerator(statistics, history)
suggestion = generator.generate_suggestions(StrategyType.BALANCED, 1)[0]

numbers = suggestion['numbers']
metadata = suggestion['metadata']

print(f"\nNumeros: {' - '.join(f'{n:02d}' for n in numbers)}")
print(f"\nValidacao:")
print(f"  - Quantidade: {len(numbers)} (esperado: 15)")
print(f"  - Minimo: {min(numbers)} (esperado: >= 1)")
print(f"  - Maximo: {max(numbers)} (esperado: <= 25)")
print(f"  - Todos validos: {all(1 <= n <= 25 for n in numbers)}")

print(f"\nEstatisticas:")
print(f"  - Pares/Impares: {metadata['even_count']}/{metadata['odd_count']}")
print(f"  - Soma: {metadata['sum']}")
print(f"  - Distribuicao: {metadata['range_distribution']}")

if len(numbers) == 15 and all(1 <= n <= 25 for n in numbers):
    print("\n" + "=" * 70)
    print("  SUCESSO! Sistema configurado corretamente para Lotofacil!")
    print("=" * 70)
else:
    print("\n" + "=" * 70)
    print("  ERRO! Numeros fora do esperado!")
    print("=" * 70)
