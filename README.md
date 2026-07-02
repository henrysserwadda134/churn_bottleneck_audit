# Fintech User Retention & Operational Bottleneck Audit
## Executive Summary
This project builds an automated data pipeline to analysze user lifecycle friction and transaction processing degradation for a retail financial platform. By extraacting and analyzing over 96,000 relational records froman isolated SQLite database, this audit isolates where user acquisition capital is wasted and quantifies structural revenue leakage


## The Core Business Bottlenecks (Identified via Data Audit)
A baseline diagnostic check of the active database infrastructure exposed two critialoperational vulnerabilities that directly impact user lifetime value (LTV) and platform trust:
### 1. Onboardinging funnel churn (41.06% KYC Failure rate)
* **The Metric:** out of 5,00 unique users who created an account, **2,053 failed the Know Your Customer (KYC) verification process**.
* **Business Impact** High marketing burn rate. The company is actively spending capital to acquire users, only for 4 out of 10 to be blocked at the front door. This indicates either an overly restrictive compliance UI or an inergration withthe third-party verification API.

### 2. Transactional Revenue Leakage (18.06% Faliure Rate)
* **The Metric:** Out of 96,704 total transaction attempts, **17,465 resulted in a hard faliure status**.
* **Business Impact:** Severe retention risk andimmediate revenue loss. In financial services, transactional instability drives users to compititors instantly. This high faliure volume indicates backend processing latency or systemic API timeouts during peak traffic.


## Project Structure & Data inffrastructure
The repository is organised to seperate data generation, operational diagnostics, and the analytical visualization layer:

* `data/`: Conatins the relational SQLite database (`database.sqlite`) and exported analytical tables.
* `src/generate_data.py`: Synthesizes the relational database scheme, populates 5,000 historical users, and engineers specificoperational anomalies (the KYC and transaction faliure bugs)
* `src/pipeline.py`: Executes the automated database extraction and output core health metrics.
* `src/cohort_analysis.py`: (in progress) Builds the programmatic cohort retention matrices.