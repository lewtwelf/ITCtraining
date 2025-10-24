from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("LewZooDataTest") \
    .config("hive.metastore.uris", "thrift://18.134.163.221:9083") \
    .enableHiveSupport() \
    .getOrCreate()

#.config("spark.sql.warehouse.dir", "hdfs:///user/Consultants/warehouse") \
# .config("hive.metastore.warehouse.external.dir", "hdfs:///user/Consultants/warehouse") \

def readout(df):
    print("+++++++++++++++++++++++ readout start +++++++++++++++++++++++")
    for row in df.collect(): 
        print(row)
    print("+++++++++++++++++++++++ readout end +++++++++++++++++++++++")

spark.sql("USE de01102025")

#spark.sql("""CREATE DATABASE IF NOT EXISTS lew_db LOCATION 'hdfs:///user/Consultants/warehouse/lew_db'""")
#spark.sql("USE lew_db")

animals = spark.sql("SELECT * FROM lew_animal_information")
feeding = spark.sql("SELECT * FROM lew_feeding_records")

#animals = spark.read.option("header", "true").csv(
#    "hdfs:///tmp/DE011025/lewtwelf/sqoop/lew_animal_information")
#feeding = spark.read.option("header", "true").csv(
#    "hdfs:///tmp/DE011025/lewtwelf/sqoop/lew_feeding_records")

from pyspark.sql.types import IntegerType, DoubleType

feeding = feeding.withColumn("quantity_kg", col("quantity_kg").cast(DoubleType()))
animals = animals.withColumn("age", col("age").cast(IntegerType()))

joined_df = animals.join(feeding, on="animal_id", how="inner")

over_5kg_df = joined_df.filter(col("quantity_kg") > 5)

result_df = over_5kg_df.select(
    "animal_id",
    "animal_name",
    "species",
    "age",
    "enclosure_id",
    "feeding_date",
    "food_type",
    "quantity_kg"
)

result_df.write.mode("overwrite") \
    .option("path", "/tmp/DE011025/lewtwelf/sqoop/") \
    .saveAsTable("lew_animal_over_5kg")

#result_df.write.mode("overwrite").saveAsTable("lew_animal_over_5kg")
#result_df.write.option("path", "/tmp/DE011025/lewtwelf/sqoop/").saveAsTable("lew_animal_over_5kg")

#readout(spark.sql("SELECT * FROM lew_animal_over_5kg"))

spark.stop()
