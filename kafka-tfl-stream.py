from pyspark.sql import SparkSession
from pyspark.sql.functions import to_json, struct
import requests
import json

# Initialize Spark session
spark = SparkSession.builder \
    .appName("TfL Kafka Producer") \
    .getOrCreate()

# API URL
api_url = "https://api.tfl.gov.uk/Line/victoria/Arrivals?app_id=92293faa428041caad3dd647d39753a0&app_key=ba72936a3db54b4ba5792dc8f7acc043"

# Get data from API
response = requests.get(api_url)
total = response.text

# Create DataFrame from JSON string
df_from_text = spark.read.json(spark.sparkContext.parallelize([total]))

# Select columns to send
message_df = df_from_text.select(
    "id",
    "stationName",
    "lineName",
    "towards",
    "expectedArrival"
)

# Write DataFrame directly to Kafka
message_df.selectExpr("CAST(id AS STRING) AS key", "to_json(struct(*)) AS value") \
    .write \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "ip-172-31-3-80.eu-west-2.compute.internal:9092") \
    .option("topic", "tfl_victoria_line") \
    .save()
