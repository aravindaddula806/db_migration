SPARK_JARS="./jars/postgresql-42.7.5.jar,./jars/hadoop-aws-3.3.4.jar,./jars/hadoop-common-3.3.4.jar,./jars/aws-java-sdk-bundle-1.12.262.jar"
host_name = 'PostgreSQL'
port=5432
db_name = 'ofbiz_srifin'

SPARK_JARS="./jars/postgresql-42.7.5.jar,./jars/hadoop-aws-3.3.4.jar,./jars/hadoop-common-3.3.4.jar,./jars/aws-java-sdk-bundle-1.12.262.jar"

dest_bucket_name = 's3a://dms-peripheral-applications-data'

base_tgt_path = f"{dest_bucket_name}/borrower_management"

# excluded_tables=['emp_salary_breakup','empl_application_detail','empl_application_detail_n6_backup','empl_application_salary_breakup']
# excluded_tables=['sessions']


log_file_dir = './logs'
excluded_schemas = "('information_schema','pg_catalog')"

''' Testing Configuration details
host_name = '192.168.80.38'
db_name = 'borrower_management'
port=5555
excluded_tables=['employee_master']
 '''