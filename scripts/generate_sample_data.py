"""
Generate sample lottery history data for testing.

This script creates a sample Excel file with 100 lottery contests
to demonstrate the system functionality.
"""

import random
from datetime import datetime, timedelta

import pandas as pd


def generate_sample_data(num_contests: int = 100) -> pd.DataFrame:
    """
    Generate sample lottery data.
    
    Args:
        num_contests: Number of contests to generate.
    
    Returns:
        DataFrame with sample lottery data.
    """
    contests = []
    start_date = datetime(2020, 1, 1)
    
    for i in range(1, num_contests + 1):
        # Generate 6 unique random numbers between 1 and 60
        numbers = random.sample(range(1, 61), 6)
        numbers.sort()  # Sort the numbers as is typical in lotteries
        
        contest = {
            "concurso": i,
            "data": (start_date + timedelta(days=i * 3)).date(),
            "bola_1": numbers[0],
            "bola_2": numbers[1],
            "bola_3": numbers[2],
            "bola_4": numbers[3],
            "bola_5": numbers[4],
            "bola_6": numbers[5],
        }
        contests.append(contest)
    
    return pd.DataFrame(contests)


if __name__ == "__main__":
    # Generate sample data
    df = generate_sample_data(100)
    
    # Save to Excel
    output_file = "data/raw/lottery_history.xlsx"
    df.to_excel(output_file, index=False)
    
    print(f"✓ Created sample lottery history with {len(df)} contests")
    print(f"✓ Saved to: {output_file}")
    print(f"\nSample data:")
    print(df.head(10))
