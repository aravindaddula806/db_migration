from pyspark.sql import SparkSession
import os,datetime
from configs import (host_name,port,dest_bucket_name,base_tgt_path,db_name,SPARK_JARS,
                     log_file_dir,excluded_tables,excluded_schemas)

# os.environ["SPARK_CONF_DIR"] = '/home/jarvis/docker_images/peripheral_apps_container/spark_defaults'
# .config("spark.driver.extraJavaOptions", "-Dconfig.resource=spark-defaults.conf") \

from Test_Files.log_writer import write_log

from dotenv import load_dotenv
load_dotenv()

access_key=os.getenv("ACCESS_KEY")
secret_key=os.getenv("SECRET_KEY")
# spark_jars=os.getenv("SPARK_JARS")
PG_USER=os.getenv("PG_USER")
PG_PASSWD=os.getenv("PG_PASSWD")

print('spark session will start')

spark = SparkSession.builder \
    .appName("Redgrape DB Migration") \
    .config("spark.jars", SPARK_JARS) \
    .config("spark.hadoop.fs.s3a.access.key", access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", secret_key) \
    .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
    .getOrCreate()

print('spark session started')

pg_jdbc_url = f"jdbc:postgresql://{host_name}:{port}/{db_name}"

connection_properties = {
    "user": PG_USER,
    "password": PG_PASSWD,
    "driver": "org.postgresql.Driver"
}

print(f'jdbc url is {pg_jdbc_url}')
def write_into_s3 (schema_name):
    # all_tables_query = f"(select tablename from pg_catalog.pg_tables where schemaname = '{schema_name}') as tables_list"
    all_tables_query = f"""
                        (select tablename from pg_catalog.pg_tables
                        where schemaname not in {excluded_schemas} and schemaname='{schema_name}') as tables_list
                        """

    all_tables = spark.read.jdbc(
        url=pg_jdbc_url,
        table=all_tables_query,
        properties=connection_properties
    )

    #collect table names as list
    final_table_names = [row.tablename for row in all_tables.collect() if row.tablename not in excluded_tables]
    # dictionary to store all the tables data into a dictionary# tables_data_dict = {}
    # read each table and store the dataframes into tables_data_dict
    for table_name in final_table_names:
        print(f'table name {table_name}')
        dest_path = f'{dest_bucket_name}/{db_name}/{schema_name}/{table_name}'
        try:
            data_df = spark.read.jdbc(url=pg_jdbc_url,table=f"{schema_name}.{table_name}",properties=connection_properties)
            # data_df.show(n=1)
            data_df.coalesce(1)\
                   .write.mode("overwrite") \
                   .parquet(dest_path)
            print(f'Writen success under {dest_path} at {datetime.datetime.now()}')

        except Exception as e:
            error_msg = f'ERROR {e}'
            # write_log(error_msg,schema_name)

print()

''' Fetch all the schemas and pass it into write s3 table function'''

all_schemas_query = f"(select distinct schemaname from pg_catalog.pg_tables where schemaname not in {excluded_schemas}) as tables_list"
all_schemas = spark.read.jdbc(
    url=pg_jdbc_url,
    table=all_schemas_query,
    properties=connection_properties
)
final_table_names = [row.schemaname for row in all_schemas.collect()]

for schema in final_table_names:
    print(f'writing at {schema}')
    write_into_s3(schema)

# spark.stop()