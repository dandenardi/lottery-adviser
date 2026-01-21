"""Check skiprows=4 in detail."""

import pandas as pd
from pathlib import Path

filepath = Path('data/raw/loto_facil_asloterias_ate_concurso_3576_sorteio.xlsx')

print("Reading with skiprows=4, header=0:")
df = pd.read_excel(filepath, skiprows=4, header=0)

print(f"\nShape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nFirst 3 rows:")
print(df.head(3))
print(f"\nColumn names (normalized):")
normalized = [str(col).strip().lower() for col in df.columns]
print(normalized)
print(f"\n'concurso' in normalized: {'concurso' in normalized}")
