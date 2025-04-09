<!-- install libraries -->
source /home/sparkuser/venv/bin/activate;
pip install dotenv pyspark==3.5.5


# redgrape_db_migration
<!-- Make configs file importable globally -->
<!-- add redgrape_db_migration folder as a pip package to get all the config variables -->

--->create setup.py file
from setuptools import setup

setup(
    name="redgrape_db_migration",
    version="0.1",
    py_modules=["configs"],  # This makes configs.py importable
)

2. execute the command inside folder
#pip install -e ~/docker_images/peripheral_apps_container
or if you are inside peripheral_apps_container directory run

pip install -e .

3.create configs.py file and place all the configurations in it.


<!-- #Jars to download and place -->

wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar ;
wget https://jdbc.postgresql.org/download/postgresql-42.7.5.jar ;
wget https://repo.maven.apache.org/maven2/org/apache/hadoop/hadoop-common/3.3.4/hadoop-common-3.3.4.jar;
wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar;
