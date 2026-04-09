"""
Script to fix the database schema by adding missing columns.
Run this on Render to sync the database with the current models.
"""

import os
import sys
from pathlib import Path
from sqlalchemy import text

# Add parent directory to path so we can import 'app'
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import engine

def fix_schema():
    print("\n" + "="*60)
    print("  DATABASE SCHEMA FIX - Adding missing columns")
    print("="*60 + "\n")
    
    with engine.connect() as conn:
        # 1. Check user_suggestion_usage table
        print("Checking 'user_suggestion_usage' table...")
        
        # Check rewarded_suggestions_count
        res = conn.execute(text("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='user_suggestion_usage' AND column_name='rewarded_suggestions_count';
        """))
        if not res.fetchone():
            print("  -> Adding 'rewarded_suggestions_count' to 'user_suggestion_usage'...")
            conn.execute(text("ALTER TABLE user_suggestion_usage ADD COLUMN rewarded_suggestions_count INTEGER DEFAULT 0;"))
            conn.commit()
            print("  [OK] Column added.")
        else:
            print("  [SKIP] Column 'rewarded_suggestions_count' already exists.")
            
        # Check is_premium in user_suggestion_usage
        res = conn.execute(text("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name='user_suggestion_usage' AND column_name='is_premium';
        """))
        if not res.fetchone():
            print("  -> Adding 'is_premium' to 'user_suggestion_usage'...")
            conn.execute(text("ALTER TABLE user_suggestion_usage ADD COLUMN is_premium BOOLEAN DEFAULT FALSE;"))
            conn.commit()
            print("  [OK] Column added.")
        else:
            print("  [SKIP] Column 'is_premium' already exists.")

        # 2. Check user_subscriptions table (just in case)
        print("\nChecking 'user_subscriptions' table...")
        # Check if table exists
        res = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'user_subscriptions');"))
        if res.fetchone()[0]:
            # Table exists, check columns
            for col, col_type in [
                ('subscription_id', 'VARCHAR'), 
                ('expires_at', 'TIMESTAMP'),
                ('is_premium', 'BOOLEAN DEFAULT FALSE')
            ]:
                res = conn.execute(text(f"SELECT column_name FROM information_schema.columns WHERE table_name='user_subscriptions' AND column_name='{col}';"))
                if not res.fetchone():
                    print(f"  -> Adding '{col}' to 'user_subscriptions'...")
                    conn.execute(text(f"ALTER TABLE user_subscriptions ADD COLUMN {col} {col_type};"))
                    conn.commit()
                    print(f"  [OK] Column '{col}' added.")
                else:
                    print(f"  [SKIP] Column '{col}' already exists.")
        else:
            print("  [SKIP] Table 'user_subscriptions' does not exist yet (will be created by app startup).")

    print("\n" + "="*60)
    print("  SCHEMA FIX COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        fix_schema()
    except Exception as e:
        print(f"\n[ERROR] Failed to fix schema: {e}")
        sys.exit(1)
