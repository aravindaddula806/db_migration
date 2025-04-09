import os
import datetime
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv
from configs import (host_name, port, dest_bucket_name, base_tgt_path, db_name,
                     log_file_dir, excluded_tables, excluded_schemas)

load_dotenv()

access_key = os.getenv("ACCESS_KEY")
secret_key = os.getenv("SECRET_KEY")
PG_USER = os.getenv("PG_USER")
PG_PASSWD = os.getenv("PG_PASSWD")

# PostgreSQL Connection URL
pg_url = f"postgresql://{PG_USER}:{PG_PASSWD}@{host_name}:{port}/{db_name}"
engine = create_engine(pg_url)

print("Connected to PostgreSQL")

def write_into_s3(schema_name):
    all_tables_query = f"""
        SELECT tablename FROM pg_catalog.pg_tables
        WHERE schemaname NOT IN {excluded_schemas} AND schemaname = '{schema_name}'
    """
    
    all_tables = pd.read_sql(all_tables_query, engine)
    final_table_names = [row['tablename'] for _, row in all_tables.iterrows() if row['tablename'] not in excluded_tables]
    
    for table_name in final_table_names:
        print(f"Processing table: {table_name}")
        dest_path = f"{dest_bucket_name}/{db_name}/{schema_name}/{table_name}.parquet"
        try:
            query = f"SELECT * FROM {schema_name}.{table_name}"
            data_df = pd.read_sql(query, engine)
            data_df.to_parquet(dest_path, index=False)
            print(f"Written to {dest_path} at {datetime.datetime.now()}")
        except Exception as e:
            print(f"Error writing {table_name}: {e}")

# Fetch all schemas
all_schemas_query = f"SELECT DISTINCT schemaname FROM pg_catalog.pg_tables WHERE schemaname NOT IN {excluded_schemas}"
all_schemas = pd.read_sql(all_schemas_query, engine)
final_schemas = [row['schemaname'] for _, row in all_schemas.iterrows()]

for schema in final_schemas:
    print(f"Writing schema: {schema}")
    write_into_s3(schema)

print("Data export completed.")