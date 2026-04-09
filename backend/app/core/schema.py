"""
Utility for ensuring the database schema is in sync with the models.
This is used as a lightweight alternative to Alembic migrations for simple schema updates.
"""

from sqlalchemy import text
from app.core.database import engine

def ensure_schema_sync():
    """
    Check for missing columns and add them if necessary.
    This runs on application startup.
    """
    print("\n" + "-"*40)
    print("Checking database schema synchronization...")
    print("-"*40)
    
    try:
        with engine.connect() as conn:
            # 1. Check user_suggestion_usage table
            print("Table: user_suggestion_usage")
            
            # Columns to check in user_suggestion_usage
            usage_columns = [
                ('rewarded_suggestions_count', 'INTEGER DEFAULT 0'),
                ('is_premium', 'BOOLEAN DEFAULT FALSE')
            ]
            
            for col, col_def in usage_columns:
                res = conn.execute(text(f"""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name='user_suggestion_usage' AND column_name='{col}';
                """))
                if not res.fetchone():
                    print(f"  -> Adding column '{col}'...")
                    conn.execute(text(f"ALTER TABLE user_suggestion_usage ADD COLUMN {col} {col_def};"))
                    conn.commit()
                    print(f"  [OK] Column '{col}' added.")
                else:
                    print(f"  [SKIP] Column '{col}' already exists.")
                    
            # 2. Check user_subscriptions table
            print("\nTable: user_subscriptions")
            # Check if table exists first
            res = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'user_subscriptions');"))
            if res.fetchone()[0]:
                sub_columns = [
                    ('subscription_id', 'VARCHAR'), 
                    ('expires_at', 'TIMESTAMP'),
                    ('is_premium', 'BOOLEAN DEFAULT FALSE')
                ]
                for col, col_def in sub_columns:
                    res = conn.execute(text(f"""
                        SELECT column_name FROM information_schema.columns 
                        WHERE table_name='user_subscriptions' AND column_name='{col}';
                    """))
                    if not res.fetchone():
                        print(f"  -> Adding column '{col}'...")
                        conn.execute(text(f"ALTER TABLE user_subscriptions ADD COLUMN {col} {col_def};"))
                        conn.commit()
                        print(f"  [OK] Column '{col}' added.")
                    else:
                        print(f"  [SKIP] Column '{col}' already exists.")
            else:
                print("  [SKIP] Table 'user_subscriptions' does not exist yet.")

        print("-"*40)
        print("Schema synchronization complete.")
        print("-"*40 + "\n")
        
    except Exception as e:
        print(f"\n[ERROR] Schema synchronization failed: {e}")
        # We don't want to crash the whole app if this fails, 
        # but the error will be visible in the logs.
        pass
