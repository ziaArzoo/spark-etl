from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from datetime import datetime, timedelta

# Default arguments for all tasks
default_args = {
    "owner": "Zia",
    "depends_on_past": False,
    "email": ["ziaarzoo21@gmail.com"],
    "email_on_failure": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

# DAG definition
with DAG(
    dag_id="weather_etl_pipeline",
    description="Airflow DAG equivalent of Databricks Weather ETL Pipeline",
    default_args=default_args,
    start_date=datetime(2025, 10, 21),
    schedule_interval="14 55 23 * * ?",  # same cron as Databricks job
    catchup=False,
    tags=["databricks", "etl", "pyspark", "delta"],
) as dag:

    # Task 1: Extract Raw
    extract_raw = DatabricksRunNowOperator(
        task_id="extract_raw",
        databricks_conn_id="databricks_default",
        job_id=123,  # Replace with actual Databricks job ID
        notebook_params={"task_key": "extract_raw"},
    )

    # Task 2: Transform Silver
    transform_silver = DatabricksRunNowOperator(
        task_id="transform_silver",
        databricks_conn_id="databricks_default",
        job_id=124,  # Replace with actual job ID
        notebook_params={"task_key": "Transform_Silver"},
    )

    # Task 3: Load Gold
    load_gold = DatabricksRunNowOperator(
        task_id="load_gold",
        databricks_conn_id="databricks_default",
        job_id=125,  # Replace with actual job ID
        notebook_params={"task_key": "Load_Gold"},
    )

    # Define task dependencies
    extract_raw >> transform_silver >> load_gold
