# 🌤️ Weather ETL Pipeline (PySpark · Delta Lake · Unity Catalog · Databricks)

[![Databricks Workflow](https://img.shields.io/badge/Databricks-Workflow-orange?logo=databricks)](./workflows/databricks_job_setup.md)
![PySpark](https://img.shields.io/badge/PySpark-ETL-brightgreen)
![Delta Lake](https://img.shields.io/badge/Storage-Delta%20Lake-blue)
![Unity Catalog](https://img.shields.io/badge/Governance-Unity%20Catalog-purple)
![Python](https://img.shields.io/badge/Python-3.x-yellow)
![Azure](https://img.shields.io/badge/Cloud-Azure-lightblue)

---

## 📘 Overview

This project implements a **distributed ETL pipeline** using **PySpark**, **Delta Lake**, and **Databricks Workflows**.  
It automates ingestion, transformation, and aggregation of weather data from REST APIs, governed under **Unity Catalog**.

The pipeline runs daily on Databricks with built-in retries, alerts, and full configuration via YAML + JSON.

---

## ⚙️ Key Features

✅ End-to-end ETL (Extract → Transform → Load)  
✅ Delta Lake ACID storage under Unity Catalog  
✅ Email alert on failure (to `ziaarzoo21@gmail.com`)  
✅ Retry once after 1 minute (includes timeout retry)  
✅ Managed Databricks Job JSON (`pipeline.json`)  
✅ Optional Airflow DAG for hybrid orchestration  
✅ Config-driven (YAML) + Git versioned notebooks  
✅ **Containerized with Docker** for reproducibility and portability 

---

## 🧩 Architecture

```
Open-Meteo REST API
        │
        ▼
 ┌────────────────────────┐
 │  Bronze (Raw)          │ →  main.weather_etl.raw_weather
 └────────────────────────┘
        │
        ▼
 ┌────────────────────────┐
 │  Silver (Curated)      │ →  main.weather_etl.silver_weather_curated
 └────────────────────────┘
        │
        ▼
 ┌────────────────────────┐
 │  Gold (Aggregated)     │ →  main.weather_etl.gold_weather_aggregates
 └────────────────────────┘
```

---

## 🧱 Tech Stack

| Category | Tools |
|-----------|--------|
| Language | Python 3 · PySpark |
| Storage | Delta Lake |
| Governance | Unity Catalog |
| Orchestration | Databricks Jobs (new UI) |
| Cloud | Azure Databricks |
| Version Control | Git + GitHub |
| Optional | Airflow DAG, Docker |

---

## 📂 Repository Structure

```
pyspark-etl/
├── config/
│   └── config.yaml
├── notebooks/
│   ├── Extract data
│   ├── Transform Data
│   └── load Data
├── src/
│   ├── extract/
│   ├── transform/
│   └── load/
├── workflow/
│   ├── pipeline.json
│   ├── pipeline_readme.md
│   └── pipeline_airflow.py
├── requirements.txt
└── README.md
```

---

## ⚡ Databricks Workflow (New UI)

**Job name:** `Weather_ETL_Pipeline`

| Setting | Value |
|----------|--------|
| Schedule | `14 55 23 * * ?` UTC (≈ 05 : 25 IST daily) |
| Max concurrent runs | 1 |
| Retry | 1 retry · 1 min interval |
| Retry on timeout | ✅ |
| Queueing | ✅ Enabled |
| Performance target | `PERFORMANCE_OPTIMIZED` |
| Email alert | `ziaarzoo21@gmail.com` |

### DAG

```
extract_raw  →  Transform_Silver  →  Load_Gold
```

To import this workflow:

1. Open **Compute → Jobs → Create Job → Import JSON**  
2. Upload `workflows/pipeline.json`  
3. Confirm notebook paths and cluster  
4. Save and run ✅

---

## ▶️ Running the Pipeline (Manual)

Each notebook automatically loads the config:


Run in order:
1. **Extract data** → creates `raw_weather`
2. **Transform Data** → creates `silver_weather_curated`
3. **load Data** → creates `gold_weather_aggregates`


---

## 🔔 Alerts & Monitoring

- Email sent on any task failure.  
- Retries once after 1 minute (backoff).  
- “Retry on timeout” enabled.  

---

## 🧠 Development Flow

1. Update code / config locally in Databricks Repos.  
2. Commit → Push to GitHub.  
3. If the workflow changes, re-export JSON and update `workflows/pipeline.json`.  
4. Run job manually or on schedule.

---

## 🌀 Airflow Integration (Optional)

An equivalent Airflow DAG is provided in  
[`workflows/airflow_weather_etl_dag.py`](./workflows/pipeline_airflow.py)

Use it if you want external orchestration via Airflow’s Databricks operators.

## 🏁 Author

**Zia** — Software developer,  
building distributed ETL systems using PySpark, Delta, and Azure Databricks.
