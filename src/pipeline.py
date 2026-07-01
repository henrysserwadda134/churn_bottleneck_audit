import sqlite3
import pandas as pd

def get_db_connection(db_path='data/database.sqlite'):
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def run_health_check():
    """Runs primary volume checks across all relational tables."""
    conn = get_db_connection()
    if conn is None:
        return

    print("--- RELATIONAL DATA HEALTH CHECK ---")
    
    # 1. Total Counts
    user_count = pd.read_sql_query("SELECT COUNT(*) as total_users FROM users;", conn)
    log_count = pd.read_sql_query("SELECT COUNT(*) as total_logs FROM activity_logs;", conn)
    tx_count = pd.read_sql_query("SELECT COUNT(*) as total_transactions FROM transactions;", conn)
    
    print(f"Total Users Loaded: {user_count['total_users'].values[0]}")
    print(f"Total Activity Logs Loaded: {log_count['total_logs'].values[0]}")
    print(f"Total Transactions Loaded: {tx_count['total_transactions'].values[0]}\n")

    # 2. Initial Funnel Diagnostic (Onboarding Verification Drop-off)
    print("--- ONBOARDING FUNNEL STAGE COUNTS ---")
    funnel_query = """
        SELECT action, COUNT(user_id) as user_count 
        FROM activity_logs 
        WHERE action IN ('account_created', 'kyc_completed', 'kyc_failed')
        GROUP BY action;
    """
    funnel_df = pd.read_sql_query(funnel_query, conn)
    print(funnel_df.to_string(index=False))
    print("\n")

    # 3. Transaction Failure Rate Diagnostic
    print("--- TRANSACTION STATUS BREAKDOWN ---")
    tx_query = """
        SELECT status, COUNT(*) as status_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions), 2) as percentage
        FROM transactions
        GROUP BY status;
    """
    tx_df = pd.read_sql_query(tx_query, conn)
    print(tx_df.to_string(index=False))

    conn.close()

if __name__ == "__main__":
    run_health_check()