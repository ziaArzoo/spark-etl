import datetime as dt
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from .api_client import APIClient


def run(cfg: dict, spark: SparkSession) -> str:
    """
    Fetch data from Open-Meteo API and write to Unity Catalog managed Delta table.
    """

    # 1️⃣ Fetch config details
    base_url = cfg["source_api"]["base_url"]
    params = cfg["source_api"]["params"]
    catalog = cfg["catalog_name"]
    schema = cfg["schema_name"]
    table_name = cfg["tables"]["raw"]
    full_table_name = f"{catalog}.{schema}.{table_name}"

    # 2️⃣ Fetch API JSON
    client = APIClient(base_url, params)
    data = client.fetch()

    # 3️⃣ Flatten JSON to records
    hourly = data.get("hourly", {})
    records = []
    for i, ts in enumerate(hourly.get("time", [])):
        records.append({
            "timestamp": ts,
            "temperature_2m": hourly.get("temperature_2m", [])[i],
            "relative_humidity_2m": hourly.get("relative_humidity_2m", [])[i],
            "precipitation": hourly.get("precipitation", [])[i],
        })

    # 4️⃣ Create DataFrame
    ingest_time = dt.datetime.utcnow()
    df = spark.createDataFrame(records)
    df = df.withColumn("ingest_ts", lit(ingest_time))
    df = df.withColumn("ingest_date", lit(ingest_time.date().isoformat()))

    # 5️⃣ Write to Unity Catalog Delta Table
    (
        df.write.format("delta")
          .mode("append")
          .option("mergeSchema", "true")
          .partitionBy(cfg["partition_column"])
          .saveAsTable(full_table_name)
    )

    print(f"✅ Data successfully written to Unity Catalog table: {full_table_name}")
    return full_table_name
