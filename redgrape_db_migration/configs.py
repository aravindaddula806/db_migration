SPARK_JARS="./jars/postgresql-42.7.5.jar,./jars/hadoop-aws-3.3.4.jar,./jars/hadoop-common-3.3.4.jar,./jars/aws-java-sdk-bundle-1.12.262.jar"
host_name = '192.168.80.38'
port=5555
SPARK_JARS="./jars/postgresql-42.7.5.jar,./jars/hadoop-aws-3.3.4.jar,./jars/hadoop-common-3.3.4.jar,./jars/aws-java-sdk-bundle-1.12.262.jar"

dest_bucket_name = 's3a://dms-peripheral-applications-data'

base_tgt_path = f"{dest_bucket_name}/borrower_management"

# db_name = 'ofbiz_srifin'
excluded_tables=['emp_salary_breakup','empl_application_detail','empl_application_detail_n6_backup','empl_application_salary_breakup']


log_file_dir = './logs'
excluded_schemas = "('information_schema','pg_catalog')"

''' Testing Configuration details '''
# schema_name='staging'
# db_name = 'borrower_management'