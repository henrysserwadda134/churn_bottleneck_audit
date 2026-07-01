import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)
num_users = 5000
conn = sqlite3.connect('data/database.sqlite')
cursor = conn.cursor()

print("Enforcing schema and creating tables...")
cursor.executescript('''
    DROP TABLE IF EXISTS activity_logs;
    DROP TABLE IF EXISTS transactions;
    DROP TABLE IF EXISTS users;

    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        signup_date TEXT,
        acquisition_channel TEXT,
        segment TEXT
    );

    CREATE TABLE transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        timestamp TEXT,
        amount REAL,
        status TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE activity_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        timestamp TEXT,
        action TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
''')

# Generate Users Table
channels = ['Organic', 'Google_Ads', 'Meta_Ads', 'Referral']
segments = ['Retail', 'Enterprise', 'Power_User']
start_date = datetime(2025, 1, 1)

user_data = []
for i in range(1, num_users + 1):
    days_offset = np.random.randint(0, 180)
    s_date = start_date + timedelta(days=days_offset)
    user_data.append((
        i, 
        s_date.strftime('%Y-%m-%d %H:%M:%S'), 
        np.random.choice(channels, p=[0.4, 0.3, 0.2, 0.1]),
        np.random.choice(segments, p=[0.7, 0.1, 0.2])
    ))

cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', user_data)

# Generate Activity Logs & Transactions
log_data = []
transaction_data = []

for u in user_data:
    uid, s_date_str, _, segment = u
    s_date = datetime.strptime(s_date_str, '%Y-%m-%d %H:%M:%S')
    log_data.append((uid, s_date.strftime('%Y-%m-%d %H:%M:%S'), 'account_created'))
    
    if np.random.rand() < 0.40:
        log_data.append(((uid, (s_date + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S'), 'kyc_failed')))
        continue 
    
    log_data.append(((uid, (s_date + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S'), 'kyc_completed')))
    active_days = np.random.randint(1, 90) if segment == 'Retail' else np.random.randint(30, 150)
    is_affected_by_bug = (s_date > datetime(2025, 4, 1)) and (np.random.rand() < 0.5)

    current_date = s_date
    for _ in range(active_days):
        current_date += timedelta(days=np.random.randint(1, 5))
        if current_date > datetime(2025, 12, 31):
            break
            
        log_data.append((uid, current_date.strftime('%Y-%m-%d %H:%M:%S'), 'app_login'))
        
        if np.random.rand() < 0.6: 
            amount = round(np.random.exponential(scale=50.0) + 5, 2)
            status = 'Success'
            if is_affected_by_bug and np.random.rand() < 0.75:
                status = 'Failed'
                log_data.append((uid, current_date.strftime('%Y-%m-%d %H:%M:%S'), 'system_error_alert'))
                
            transaction_data.append((None, uid, current_date.strftime('%Y-%m-%d %H:%M:%S'), amount, status))

print("Populating transaction and activity tables...")
cursor.executemany('INSERT INTO transactions VALUES (?, ?, ?, ?, ?)', transaction_data)
cursor.executemany('INSERT INTO activity_logs (user_id, timestamp, action) VALUES (?, ?, ?)', log_data)

conn.commit()
conn.close()
print("Database seed complete. Location: data/database.sqlite")