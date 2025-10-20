# 🚀 Databricks Workflow — Weather ETL Pipeline

## 📄 Overview
The **Weather_ETL_Pipeline** orchestrates an end-to-end PySpark data pipeline using **Databricks Workflows** and **Delta Lake**.

It automates three core stages of the ETL lifecycle:

| Stage | Task Key | Notebook Path | Description |
|--------|-----------|----------------|--------------|
| 🟤 Extract | `extract_raw` | `/Repos/ziaarzoo21@gmail.com/spark-etl/notebooks/Extract data` | Fetches weather data from REST API and loads into the Bronze (raw) Delta table. |
| ⚪ Transform | `Transform_Silver` | `/Repos/ziaarzoo21@gmail.com/spark-etl/notebooks/Transform Data` | Cleans, validates, and structures data into the Silver (curated) table. |
| 🟡 Load | `Load_Gold` | `/Repos/ziaarzoo21@gmail.com/spark-etl/notebooks/load Data` | Aggregates metrics (avg temperature, humidity, precipitation) into the Gold analytics table. |

---

## ⚙️ Configuration Summary
| Parameter | Value |
|------------|--------|
| **Job name** | `Weather_ETL_Pipeline` |
| **Max concurrent runs** | 1 |
| **Retries per task** | 1 |
| **Retry interval** | 1 minute |
| **Retry on timeout** | ✅ Enabled |
| **Auto optimization** | ✅ Enabled (Serverless) |
| **Queueing** | ✅ Enabled |
| **Performance Target** | `PERFORMANCE_OPTIMIZED` |
| **Run as** | `ziaarzoo21@gmail.com` |

---

## 🕒 Schedule
| Setting | Value |
|----------|--------|
| **Cron Expression** | `14 55 23 * * ?` |
| **Timezone** | `UTC` |
| **Status** | Active (Unpaused) |
| **Trigger Time** | 23:55:14 UTC (05:25:14 IST daily) |

---

## 📧 Notifications
| Event | Recipient |
|--------|------------|
| On failure | `ziaarzoo21@gmail.com` |

The job sends an **email alert** if any task fails.

---

## 🔁 Retry Policy
- **1 retry per task**
- **Wait 1 minute between retries**
- **Retries on timeout:** Enabled  
- **Serverless auto-optimization:** Enabled (up to 3 additional retries)

---

## 📊 DAG Structure

Extract_Raw --> Transform_Silver --> Load_Gold

