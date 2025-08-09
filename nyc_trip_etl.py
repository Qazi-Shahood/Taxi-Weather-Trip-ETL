# Databricks notebook source
# MAGIC %md
# MAGIC Bronze Layer

# COMMAND ----------

from pyspark.sql import SparkSession, functions as F
from pyspark.sql.functions import to_date, col, udf, from_unixtime, split, date_format, unix_timestamp

spark = SparkSession.builder.appName("NYC_Trip_ETL").getOrCreate()

trip_df = spark.read.parquet("/Volumes/workspace/nyc_trips_etl/bronze_layer/yellow_tripdata.parquet", inferSchema=True, header=True)
weather_df = spark.read.csv('/Volumes/workspace/nyc_trips_etl/bronze_layer/weather.csv', inferSchema=True, header=True)


# COMMAND ----------

# MAGIC %md
# MAGIC Silver Layer

# COMMAND ----------

trip_df = trip_df.drop('store_and_fwd_flag', "Airport_fee", "DOLocationID", "PULocationID", "RatecodeID", "congestion_surcharge", "extra", "mta_tax", "payment_type", "tolls_amount", "improvement_surcharge", "congestion", "fare_amount", "tip_amount")
weather_df = weather_df.drop("DEWP", "FRSHTT", "MXSPD", "SLP", "SNDP", "STP", "VISIB", "WDSP", "GUST", "STATION")


# COMMAND ----------

trip_df = (
    trip_df
    .na.drop()
    .filter(trip_df.passenger_count > 0)
)

weather_dfd = (
    weather_df
    .na.drop()   
)

# COMMAND ----------

trip_df = (
    trip_df
    .withColumn(
    'trip_duartion', 
    ((unix_timestamp('tpep_dropoff_datetime') - unix_timestamp('tpep_pickup_datetime')) / 60).cast('int')
    ) 
    .withColumn('pickup_date',date_format(col("tpep_pickup_datetime"), "yyyy-MM-dd"))
    .drop('tpep_pickup_datetime')
    .drop('tpep_dropoff_datetime')
)

weather_df.write.format("delta").mode("overwrite").save("/Volumes/workspace/nyc_trips_etl/silver_layer/weather_cleaned")
trip_df.write.format("delta").mode("overwrite").option('mergeSchema', 'true').save("/Volumes/workspace/nyc_trips_etl/silver_layer/trip_cleaned")

# COMMAND ----------

# MAGIC %md
# MAGIC Gold Layer

# COMMAND ----------

weather_cleaned_df = spark.read.format("delta").load("/Volumes/workspace/nyc_trips_etl/silver_layer/weather_cleaned")
trip_cleaned_df = spark.read.format("delta").load("/Volumes/workspace/nyc_trips_etl/silver_layer/trip_cleaned")
display(weather_cleaned_df.limit(5))
display(trip_cleaned_df.limit(5))

# COMMAND ----------

from pyspark.sql import functions as F

merged_df = weather_cleaned_df.join(trip_cleaned_df, 
                                    trip_cleaned_df.pickup_date == weather_cleaned_df.DATE, 'inner')
merged_df = merged_df.groupBy('pickup_date', 'PRCP') \
    .agg(
        F.count('*').alias('trip_count'),
        F.avg('trip_duartion').alias('avg_duration').cast('int'),
        F.avg('total_amount').alias('avg_fare').cast('int')
    )
display(merged_df.limit(5))
merged_df.write.format("delta").mode("overwrite").option('mergeSchema', 'true').save("/Volumes/workspace/nyc_trips_etl/gold_layer/taxi_weather_delta")

# COMMAND ----------

# Example: Compare fares on rainy vs. clear days
display(merged_df.groupBy("PRCP").agg(avg("avg_fare").alias("mean_fare")))
