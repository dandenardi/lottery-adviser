"""
Shared Lottery Constants

This module contains lottery-specific constants that are shared
across the API and mobile applications.
"""

# Lotofácil Configuration
LOTTERY_MIN_NUMBER = 1
LOTTERY_MAX_NUMBER = 25
NUMBERS_PER_GAME = 15

# Strategy Settings
DEFAULT_SUGGESTIONS_COUNT = 3
RECENT_DRAWS_WINDOW = 10  # Number of recent draws to analyze for patterns

# Data Paths (relative to packages/shared/)
HISTORICAL_DATA_FILENAME = "loto_facil_asloterias_ate_concurso_3576_sorteio.xlsx"
