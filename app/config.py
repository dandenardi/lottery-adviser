"""
Configuration module for the Lottery Adviser application.

This module centralizes all configuration settings and paths used throughout the application.
"""

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Default file paths
LOTTERY_HISTORY_FILE = RAW_DATA_DIR / "loto_facil_asloterias_ate_concurso_3576_sorteio.xlsx"

# Lottery-specific settings (Lotofácil)
LOTTERY_MIN_NUMBER = 1
LOTTERY_MAX_NUMBER = 25
NUMBERS_PER_GAME = 15

# Strategy generation settings
DEFAULT_SUGGESTIONS_COUNT = 3
RECENT_DRAWS_WINDOW = 10  # Number of recent draws to analyze for patterns

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
