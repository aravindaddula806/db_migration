import boto3,os
from dotenv import load_dotenv
from configs import (host_name, port, dest_bucket_name, db_name,
                     log_file_dir, excluded_tables, excluded_schemas)

load_dotenv()

# access_key = os.getenv("ACCESS_KEY")
# secret_key = os.getenv("SECRET_KEY")
PG_USER = os.getenv("PG_USER")
PG_PASSWD = os.getenv("PG_PASSWD")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
)

dest_bucket_name = 's3://dms-peripheral-applications-data'

base_tgt_path = f"{dest_bucket_name}/borrower_management"

s3.put_object(Bucket=base_tgt_path, Key="test-file.txt", Body="Hello, S3!")
