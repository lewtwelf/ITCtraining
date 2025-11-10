from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_json, struct
import requests
from kafka import KafkaProducer

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
    col("id"),
    col("stationName"),
    col("lineName"),
    col("towards"),
    col("expectedArrival")
)

# Convert DataFrame to JSON strings
mess
