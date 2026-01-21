"""
Generate Lottery Number Suggestions - CLI Script

This script generates lottery number suggestions using various strategies
based on historical data analysis.
"""

import json
import sys
from pathlib import Path

from app.analysis.statistics_service import LotteryStatisticsService
from app.analysis.strategy_generator import LotteryStrategyGenerator, StrategyType
from app.storage.history_repository import LotteryHistoryRepository
from app.config import (
    LOTTERY_HISTORY_FILE,
    PROCESSED_DATA_DIR,
    DEFAULT_SUGGESTIONS_COUNT,
)


def print_banner():
    """Print welcome banner."""
    print("\n" + "=" * 60)
    print("  🎰 LOTOFÁCIL - GERADOR DE SUGESTÕES DE NÚMEROS 🎰")
    print("=" * 60 + "\n")


def print_strategy_menu():
    """Print strategy selection menu."""
    print("Escolha a estratégia para gerar sugestões:\n")
    print("  1. 🎯 Balanceada (Recomendada)")
    print("     → Mix equilibrado de números quentes, frios e aleatórios")
    print()
    print("  2. 🔥 Hot Numbers")
    print("     → Prioriza números mais frequentes no histórico")
    print()
    print("  3. ❄️  Cold Numbers")
    print("     → Prioriza números menos frequentes (atrasados)")
    print()
    print("  4. 🎲 Aleatória Ponderada")
    print("     → Seleção aleatória baseada em probabilidades históricas")
    print()
    print("  5. 📈 Padrões Recentes")
    print("     → Analisa tendências dos últimos sorteios")
    print()


def get_strategy_choice() -> StrategyType:
    """
    Get strategy choice from user.
    
    Returns:
        Selected StrategyType
    """
    while True:
        try:
            choice = input("Digite o número da estratégia (1-5): ").strip()
            
            strategy_map = {
                "1": StrategyType.BALANCED,
                "2": StrategyType.HOT_NUMBERS,
                "3": StrategyType.COLD_NUMBERS,
                "4": StrategyType.WEIGHTED_RANDOM,
                "5": StrategyType.RECENT_PATTERNS,
            }
            
            if choice in strategy_map:
                return strategy_map[choice]
            else:
                print("❌ Opção inválida. Por favor, escolha entre 1 e 5.\n")
        except KeyboardInterrupt:
            print("\n\n👋 Operação cancelada pelo usuário.")
            sys.exit(0)


def get_suggestions_count() -> int:
    """
    Get number of suggestions to generate.
    
    Returns:
        Number of suggestions
    """
    while True:
        try:
            count_input = input(f"\nQuantas sugestões deseja gerar? (padrão: {DEFAULT_SUGGESTIONS_COUNT}): ").strip()
            
            if not count_input:
                return DEFAULT_SUGGESTIONS_COUNT
            
            count = int(count_input)
            if 1 <= count <= 10:
                return count
            else:
                print("❌ Por favor, escolha um número entre 1 e 10.\n")
        except ValueError:
            print("❌ Por favor, digite um número válido.\n")
        except KeyboardInterrupt:
            print("\n\n👋 Operação cancelada pelo usuário.")
            sys.exit(0)


def format_numbers(numbers: list) -> str:
    """
    Format numbers for display.
    
    Args:
        numbers: List of lottery numbers
        
    Returns:
        Formatted string
    """
    return " - ".join(f"{num:02d}" for num in numbers)


def print_suggestion(suggestion: dict, index: int):
    """
    Print a single suggestion with metadata.
    
    Args:
        suggestion: Suggestion dictionary
        index: Suggestion number (1-indexed)
    """
    print(f"\n{'─' * 60}")
    print(f"  SUGESTÃO #{index}")
    print(f"{'─' * 60}")
    print(f"\n  Números: {format_numbers(suggestion['numbers'])}")
    print(f"\n  Estratégia: {suggestion['strategy']}")
    
    metadata = suggestion['metadata']
    print(f"\n  📊 Estatísticas:")
    print(f"     • Números quentes: {metadata['hot_numbers_count']}")
    print(f"     • Números frios: {metadata['cold_numbers_count']}")
    print(f"     • Pares: {metadata['even_count']} | Ímpares: {metadata['odd_count']}")
    print(f"     • Soma total: {metadata['sum']}")
    print(f"     • Score de qualidade: {metadata['quality_score']:.2f}")
    
    print(f"\n  📍 Distribuição por faixa:")
    for range_name, count in metadata['range_distribution'].items():
        print(f"     • {range_name}: {count} números")


def save_suggestions(suggestions: list, strategy_name: str):
    """
    Save suggestions to JSON file.
    
    Args:
        suggestions: List of suggestions
        strategy_name: Name of the strategy used
    """
    timestamp = suggestions[0]['generated_at'].replace(':', '-').split('.')[0]
    filename = f"suggestions_{strategy_name}_{timestamp}.json"
    filepath = PROCESSED_DATA_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(suggestions, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Sugestões salvas em: {filepath}")


def main():
    """Main execution function."""
    try:
        print_banner()
        
        # Load historical data
        print("📂 Carregando dados históricos...")
        repository = LotteryHistoryRepository(LOTTERY_HISTORY_FILE)
        history = repository.load_history()
        print(f"✅ {len(history)} concursos carregados\n")
        
        # Compute statistics
        print("📊 Calculando estatísticas...")
        stats_service = LotteryStatisticsService()
        statistics = stats_service.compute_statistics(history)
        print(f"✅ Análise concluída ({statistics['total_numbers_analyzed']} números analisados)\n")
        
        # Show strategy menu
        print_strategy_menu()
        
        # Get user choices
        strategy = get_strategy_choice()
        count = get_suggestions_count()
        
        # Generate suggestions
        print(f"\n🎲 Gerando {count} sugestão(ões) usando estratégia '{strategy.value}'...\n")
        generator = LotteryStrategyGenerator(statistics, history)
        suggestions = generator.generate_suggestions(strategy, count)
        
        # Display suggestions
        for i, suggestion in enumerate(suggestions, 1):
            print_suggestion(suggestion, i)
        
        print(f"\n{'=' * 60}\n")
        
        # Ask to save
        save_choice = input("💾 Deseja salvar essas sugestões? (s/N): ").strip().lower()
        if save_choice in ['s', 'sim', 'y', 'yes']:
            save_suggestions(suggestions, strategy.value)
        
        print("\n✨ Boa sorte! 🍀\n")
        
    except FileNotFoundError as e:
        print(f"\n❌ Erro: {e}")
        print("\n💡 Dica: Certifique-se de que o arquivo de histórico existe em:")
        print(f"   {LOTTERY_HISTORY_FILE}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
