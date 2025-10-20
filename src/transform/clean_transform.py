from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, to_timestamp, hour, dayofmonth, month, year
)
import datetime as dt

def run(cfg: dict, spark: SparkSession):
    """
    Transform raw weather data into a curated Silver table.
    Cleans, normalizes, and enriches the dataset.
    """

    catalog = cfg["catalog_name"]
    schema = cfg["schema_name"]
    table_raw = f"{catalog}.{schema}.{cfg['tables']['raw']}"
    table_silver = f"{catalog}.{schema}.{cfg['tables']['silver']}"

    print(f"🔄 Reading from raw table: {table_raw}")
    df = spark.table(table_raw)

    # 1️⃣ Basic cleaning
    df_clean = (
        df.dropna(subset=["temperature_2m", "relative_humidity_2m"])
          .dropDuplicates(["timestamp"])
    )

    # 2️⃣ Convert timestamp & derive time-based fields
    df_clean = (
        df_clean
        .withColumn("timestamp", to_timestamp("timestamp"))
        .withColumn("hour", hour(col("timestamp")))
        .withColumn("day", dayofmonth(col("timestamp")))
        .withColumn("month", month(col("timestamp")))
        .withColumn("year", year(col("timestamp")))
    )

    #  Enforce expected schema (cast to proper types)
    df_final = (
        df_clean
        .withColumn("temperature_2m", col("temperature_2m").cast("double"))
        .withColumn("relative_humidity_2m", col("relative_humidity_2m").cast("double"))
        .withColumn("precipitation", col("precipitation").cast("double"))
    )

    #  Add ingest metadata
    df_final = df_final.withColumn("transform_ts", col("ingest_ts"))
    df_final = df_final.withColumn("transform_date", col("ingest_date"))

    # Write curated data to Silver table (overwrite for now)
    (
        df_final.write.format("delta")
          .mode("overwrite")
          .option("overwriteSchema", "true")
          .saveAsTable(table_silver)
    )

    print(f"✅ Silver table created: {table_silver}")
    return table_silver
