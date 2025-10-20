from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, sum as _sum
import datetime as dt

def run(cfg: dict, spark: SparkSession):
    """
    Aggregates curated Silver data into Gold summary table.
    Produces monthly average temperature, humidity, and total precipitation.
    """

    catalog = cfg["catalog_name"]
    schema = cfg["schema_name"]
    table_silver = f"{catalog}.{schema}.{cfg['tables']['silver']}"
    table_gold = f"{catalog}.{schema}.{cfg['tables']['gold']}"

    print(f"🔄 Reading curated data from Silver table: {table_silver}")
    df_silver = spark.table(table_silver)

    # 1️⃣ Group by Year-Month
    df_gold = (
        df_silver.groupBy("year", "month")
        .agg(
            avg(col("temperature_2m")).alias("avg_temperature"),
            avg(col("relative_humidity_2m")).alias("avg_humidity"),
            _sum(col("precipitation")).alias("total_precipitation")
        )
        .withColumn("created_at", col("transform_ts"))
    )

    # 2️⃣ Write to Gold table (overwrite for reproducibility)
    (
        df_gold.write.format("delta")
          .mode("overwrite")
          .option("overwriteSchema", "true")
          .saveAsTable(table_gold)
    )

    print(f"✅ Gold aggregate table created: {table_gold}")
    return table_gold
