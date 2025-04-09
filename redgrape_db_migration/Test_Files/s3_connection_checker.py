from pyspark.sql import SparkSession
import os,datetime
from configs import (host_name,port,dest_bucket_name,base_tgt_path,db_name,
                     log_file_dir,excluded_tables,excluded_schemas)
from py4j.java_gateway import java_import

# os.environ["SPARK_CONF_DIR"] = '/home/jarvis/docker_images/peripheral_apps_container/spark_defaults'
# .config("spark.driver.extraJavaOptions", "-Dconfig.resource=spark-defaults.conf") \

from Test_Files.log_writer import write_log

from dotenv import load_dotenv
load_dotenv()

access_key=os.getenv("ACCESS_KEY")
secret_key=os.getenv("SECRET_KEY")
spark_jars=os.getenv("SPARK_JARS")
PG_USER=os.getenv("PG_USER")
PG_PASSWD=os.getenv("PG_PASSWD")

print(f'jars are {spark_jars}')

spark = SparkSession.builder \
    .appName("Redgrape DB Migration") \
    .config("spark.jars", "./jars/postgresql-42.7.5.jar,./jars/hadoop-aws-3.4.1.jar,./jars/aws-java-sdk-bundle-1.12.262.jar") \
    .config("spark.hadoop.fs.s3a.access.key", access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", secret_key) \
    .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
    .getOrCreate()

print('spark session started')

# Ensure necessary Hadoop classes are available in Spark
java_import(spark._jvm, 'org.apache.hadoop.fs.FileSystem')
java_import(spark._jvm, 'org.apache.hadoop.fs.Path')


# Get Hadoop Configuration
hadoop_conf = spark._jsc.hadoopConfiguration()
fs = spark._jvm.FileSystem.get(hadoop_conf)

# List files in the directory
path = spark._jvm.Path(dest_bucket_name)
file_status = fs.listStatus(path)

# Count files (excluding directories)
file_count = sum(1 for file in file_status if not file.isDirectory())

print(f"Total number of files in {dest_bucket_name}: {file_count}")