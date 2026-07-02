import sqlite3
import pandas as pd
import numpy as np

def calculate_cohort_retention(db_path='data/database.sqlite'):
    """Extracts, calculates, and exports monthly cohort retention matrices."""
    conn = sqlite3.connect(db_path)
    if conn is None:
        return
        
    query = """
    WITH user_cohorts AS (
        SELECT 
            user_id,
            strftime('%Y-%m', signup_date) AS cohort_month
        FROM users
    ),
    user_activity AS (
        SELECT 
            DISTINCT log.user_id,
            strftime('%Y-%m', log.timestamp) AS activity_month
        FROM activity_logs log
        WHERE log.action = 'app_login'
    )
    SELECT 
        c.cohort_month,
        a.activity_month,
        COUNT(DISTINCT c.user_id) AS active_users
    FROM user_cohorts c
    JOIN user_activity a ON c.user_id = a.user_id
    GROUP BY 1, 2;
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    df['cohort_month'] = pd.to_datetime(df['cohort_month'] + '-01')
    df['activity_month'] = pd.to_datetime(df['activity_month'] + '-01')
    
    df['period'] = ((df['activity_month'].dt.year - df['cohort_month'].dt.year) * 12 + 
                    (df['activity_month'].dt.month - df['cohort_month'].dt.month))
    
    df['cohort_month'] = df['cohort_month'].dt.strftime('%Y-%m')
    
    cohort_matrix = df.pivot(index='cohort_month', columns='period', values='active_users').fillna(0)
    
    cohort_sizes = cohort_matrix.iloc[:, 0]
    retention_matrix = cohort_matrix.divide(cohort_sizes, axis=0)
    
    print("\n--- COHORT RETENTION MATRIX (%) ---")
    print((retention_matrix * 100).round(1).to_string())
    
    cohort_matrix.to_csv('data/cohort_counts.csv')
    retention_matrix.to_csv('data/cohort_retention.csv')
    print("\nMatrices successfully exported to data/ directory.")

if __name__ == "__main__":
    calculate_cohort_retention()