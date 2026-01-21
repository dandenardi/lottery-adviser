"""
CLI Entrypoint - Run the lottery analysis pipeline.

This script serves as the command-line interface for running
the lottery analysis pipeline and displaying results.
"""

import json
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.pipelines import run_pipeline


def format_statistics(stats: dict) -> str:
    """
    Format statistics for human-readable console output.
    
    Args:
        stats: Statistics dictionary from the pipeline.
    
    Returns:
        str: Formatted string for console display.
    """
    if "error" in stats:
        return f"❌ Error: {stats['error']}"

    output = []
    output.append("\n" + "=" * 70)
    output.append("LOTTERY STATISTICS REPORT")
    output.append("=" * 70)

    # Basic info
    output.append(f"\n📊 Total Contests Analyzed: {stats['total_contests']}")
    output.append(f"📅 Date Range: {stats['date_range']['first_draw']} to {stats['date_range']['last_draw']}")
    output.append(f"🔢 Total Numbers Analyzed: {stats['total_numbers_analyzed']}")

    # Most common numbers
    output.append("\n🔥 Most Common Numbers (Top 10):")
    for item in stats["most_common_numbers"]:
        output.append(f"   {item['number']:2d} - appeared {item['frequency']:3d} times")

    # Least common numbers
    output.append("\n❄️  Least Common Numbers (Bottom 10):")
    for item in stats["least_common_numbers"]:
        output.append(f"   {item['number']:2d} - appeared {item['frequency']:3d} times")

    # Even/Odd distribution
    output.append("\n⚖️  Even/Odd Distribution:")
    even_dist = stats["even_odd_distribution"]
    output.append(f"   Even: {even_dist['even']} ({even_dist['even_percentage']}%)")
    output.append(f"   Odd:  {even_dist['odd']} ({even_dist['odd_percentage']}%)")

    # Number range distribution
    output.append("\n📈 Number Range Distribution:")
    for range_name, count in stats["number_range_distribution"].items():
        output.append(f"   {range_name}: {count}")

    # Average sum
    output.append(f"\n💰 Average Sum of Numbers: {stats['average_sum']:.2f}")

    output.append("\n" + "=" * 70)
    output.append("")

    return "\n".join(output)


def main():
    """
    Main entry point for the CLI.
    """
    print("\n🎰 Lottery Adviser - Statistical Analysis")
    print("=" * 70)

    try:
        # Run the pipeline
        stats = run_pipeline()

        # Display formatted results
        print(format_statistics(stats))

        # Optionally save to JSON
        output_file = project_root / "data" / "processed" / "latest_statistics.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print(f"📁 Full statistics saved to: {output_file}")

        return 0

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Tip: Make sure you have a 'lottery_history.xlsx' file in the data/raw/ directory")
        return 1

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
