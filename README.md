# FinTech User Retention & Operational Bottleneck Data Pipeline

##  Executive Summary
This project engineers an automated end-to-end data pipeline to diagnose user lifecycle friction, onboarding degradation, and transactional system vulnerabilities for a retail financial services platform. By architecting a local relational database and deploying programmatic extraction and analysis layers, this audit isolates where user acquisition capital is wasted and quantifies structural revenue leakage.

##  Phase 1: Relational Data Infrastructure & Engineering
To simulate a live production environment, an isolated relational database layer was built from scratch.

### 1. Database Schema Architecture
The infrastructure consists of three highly indexed tables deployed via SQLite (`data/database.sqlite`):
* **`users` Table:** Fields include `user_id` (Primary Key), `signup_date`, and `country`. Holds the baseline cohort demographics for 5,000 synthetic profiles.
* **`activity_logs` Table:** Fields include `log_id` (Primary Key), `user_id` (Foreign Key), `timestamp`, and `action`. Tracks user behavior (e.g., system logins, onboarding attempts).
* **`transactions` Table:** Fields include `tx_id` (Primary Key), `user_id` (Foreign Key), `timestamp`, `amount`, and `status` (`Success` / `Failed`). Logs financial events.

### 2. Engineering Constraints & Debugging
* **Command Interception Block:** Resolved a Windows system conflict where default execution aliases hijacked the execution path, successfully routing compilation through the universal Python launcher (`py`).
* **Database Constraint Fix:** Corrected a critical relational insert failure in `src/generate_data.py`. The initial automated pipeline attempted to load a 3-value array directly into the 4-column `activity_logs` table, triggering an operational schema mismatch. The execution logic was restructured to explicitly declare target destinations, allowing the database engine to handle autoincrementing keys natively:
  ```python
  cursor.executemany('INSERT INTO activity_logs (user_id, timestamp, action) VALUES (?, ?, ?)', log_data)