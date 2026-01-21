"""
Script to migrate data from Excel to PostgreSQL database.

This script should be run once to populate the database with historical data.
"""

import sys
from pathlib import Path
import pandas as pd
from sqlalchemy.orm import Session

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal, engine, Base
from app.models.lottery import LotteryResult


def load_excel_data(file_path: str) -> pd.DataFrame:
    """Load lottery data from Excel file."""
    print(f"📂 Loading data from {file_path}...")
    
    # Try different skip rows (Lotofácil format)
    for skip in [6, 0]:
        try:
            df = pd.read_excel(file_path, skiprows=skip)
            df.columns = [str(col).strip().lower() for col in df.columns]
            
            if any('concurso' in col for col in df.columns):
                print(f"✅ Found valid data with skiprows={skip}")
                break
        except Exception:
            continue
    
    # Rename concurso column
    for i, col in enumerate(df.columns):
        if 'concurso' in str(col).lower():
            df.columns.values[i] = 'concurso'
            break
    
    print(f"📊 Loaded {len(df)} contests")
    return df


def migrate_data(df: pd.DataFrame, db: Session):
    """Migrate data from DataFrame to database."""
    print("🔄 Migrating data to database...")
    
    # Identify number columns
    number_columns = [col for col in df.columns if 'bola' in str(col).lower()]
    
    if not number_columns:
        # Try to find numeric columns
        number_columns = [
            col for col in df.columns
            if col not in ['concurso', 'data'] and pd.api.types.is_numeric_dtype(df[col])
        ]
    
    print(f"📍 Found {len(number_columns)} number columns")
    
    migrated = 0
    skipped = 0
    
    for _, row in df.iterrows():
        contest_number = int(row['concurso'])
        
        # Check if already exists
        existing = db.query(LotteryResult).filter(
            LotteryResult.contest_number == contest_number
        ).first()
        
        if existing:
            skipped += 1
            continue
        
        # Extract numbers
        numbers = []
        for col in number_columns:
            if pd.notna(row[col]):
                numbers.append(int(row[col]))
        
        # Get date
        draw_date = pd.to_datetime(row['data']).date() if 'data' in row else None
        
        # Create result
        result = LotteryResult(
            contest_number=contest_number,
            draw_date=draw_date,
            numbers=sorted(numbers)
        )
        
        db.add(result)
        migrated += 1
        
        if migrated % 100 == 0:
            print(f"  ✓ Migrated {migrated} contests...")
            db.commit()
    
    db.commit()
    print(f"\n✅ Migration complete!")
    print(f"   • Migrated: {migrated} contests")
    print(f"   • Skipped (already exists): {skipped} contests")


def main():
    """Main migration function."""
    print("\n" + "="*60)
    print("  📊 LOTTERY DATA MIGRATION - Excel to PostgreSQL")
    print("="*60 + "\n")
    
    # Excel file path (adjust as needed)
    excel_file = Path("../lottery-adviser/data/raw/loto_facil_asloterias_ate_concurso_3576_sorteio.xlsx")
    
    if not excel_file.exists():
        print(f"❌ Error: Excel file not found at {excel_file}")
        print("\n💡 Please update the file path in this script.")
        sys.exit(1)
    
    # Create tables
    print("🗄️  Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created\n")
    
    # Load data
    df = load_excel_data(str(excel_file))
    
    # Migrate
    db = SessionLocal()
    try:
        migrate_data(df, db)
    finally:
        db.close()
    
    print("\n🎉 All done!\n")


if __name__ == "__main__":
    main()
