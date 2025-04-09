from pyspark.sql import SparkSession
import os,datetime
from configs import SPARK_JARS
# (port,dest_bucket_name,base_tgt_path,db_name,
#                      log_file_dir,excluded_tables,excluded_schemas)

# from Test_Files.log_writer import write_log

from dotenv import load_dotenv
load_dotenv()

# spark_jars=os.getenv("SPARK_JARS","/jars/postgresql-42.7.5.jar,/jars/hadoop-aws-3.4.1.jar,/jars/aws-java-sdk-bundle-1.12.262.jar")


access_key=os.getenv("ACCESS_KEY")
secret_key=os.getenv("SECRET_KEY")
# spark_jars=os.getenv("SPARK_JARS")
PG_USER=os.getenv("PG_USER")
PG_PASSWD=os.getenv("PG_PASSWD")

print('spark session will start')
    # .config("spark.jars.packages","org.apache.hadoop:hadoop-aws:3.3.5,software.amazon.awssdk:bundle:2.20.112") \

spark = SparkSession.builder \
    .appName("Redgrape DB Migration") \
    .config("spark.jars", SPARK_JARS) \
    .config("spark.hadoop.fs.s3a.access.key", access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", secret_key) \
    .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
    .getOrCreate()

spark._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

spark.sparkContext.setLogLevel('ERROR')
# spark.sparkContext.setLogLevel('DEBUG')
print('spark session started')

# print("\n".join(spark.sparkContext._conf.get("spark.driver.extraClassPath", "").split(":")))

def read_from_s3 (bkt_url):
    try:
        df=spark.read.parquet(bkt_url)
        df.show(n=1)
        # print(f'Writen success under {dest_path} at {datetime.datetime.now()}')
    except Exception as e:
        error_msg = f'ERROR {e}'
        print(f'ERROR MESSAGE - {error_msg}')
        # write_log(error_msg,schema_name)
print()

''' Fetch all the schemas and pass it into write s3 table function'''
# bucket='s3a://dms-peripheral-applications-data/query_logs/emplog/'
bucket = 's3a://dms-peripheral-applications-data/ofbiz_srifin/monitoring/form_submission/'

read_from_s3(bucket)

spark.stop()