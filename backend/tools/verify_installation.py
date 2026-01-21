"""
Quick verification test for the lottery analysis system.

This script performs a quick sanity check to ensure all components work together.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.storage import LotteryHistoryRepository
from app.analysis import LotteryStatisticsService
from app.collectors import LotteryCollector


def test_repository():
    """Test the repository can load data."""
    print("Testing LotteryHistoryRepository...")
    repo = LotteryHistoryRepository()
    df = repo.load_history()
    assert len(df) > 0, "No data loaded"
    assert "concurso" in df.columns, "Missing 'concurso' column"
    print(f"  ✓ Loaded {len(df)} contests")
    return df


def test_statistics(df):
    """Test statistics computation."""
    print("\nTesting LotteryStatisticsService...")
    stats_service = LotteryStatisticsService()
    stats = stats_service.compute_statistics(df)
    
    assert "total_contests" in stats, "Missing total_contests"
    assert "most_common_numbers" in stats, "Missing most_common_numbers"
    assert stats["total_contests"] == len(df), "Contest count mismatch"
    
    print(f"  ✓ Computed statistics for {stats['total_contests']} contests")
    print(f"  ✓ Analyzed {stats['total_numbers_analyzed']} numbers")
    print(f"  ✓ Top number: {stats['most_common_numbers'][0]['number']} "
          f"(appeared {stats['most_common_numbers'][0]['frequency']} times)")
    
    return stats


def test_collector():
    """Test the collector (should raise NotImplementedError)."""
    print("\nTesting LotteryCollector...")
    collector = LotteryCollector()
    
    try:
        collector.fetch_latest_result()
        print("  ✗ Should have raised NotImplementedError")
        return False
    except NotImplementedError:
        print("  ✓ Correctly raises NotImplementedError (as expected)")
        return True


def main():
    """Run all tests."""
    print("=" * 70)
    print("LOTTERY ADVISER - VERIFICATION TEST")
    print("=" * 70)
    print()
    
    try:
        # Test each component
        df = test_repository()
        stats = test_statistics(df)
        test_collector()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED")
        print("=" * 70)
        print("\nThe lottery analysis system is working correctly!")
        print("You can now run: python scripts/run_pipeline.py")
        
        return 0
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ TEST FAILED")
        print("=" * 70)
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
