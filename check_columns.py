"""Check column names in loaded data."""

from pathlib import Path
from app.storage.history_repository import LotteryHistoryRepository

repo = LotteryHistoryRepository(Path('data/raw/loto_facil_asloterias_ate_concurso_3576_sorteio.xlsx'))
history = repo.load_history()

print(f"Columns ({len(history.columns)}):")
for i, col in enumerate(history.columns):
    print(f"  {i}: '{col}'")

print(f"\nFirst row:")
print(history.iloc[0])
