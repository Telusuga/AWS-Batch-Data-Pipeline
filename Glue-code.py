import sys
import os
import subprocess
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
  
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
dyf = glueContext.create_dynamic_frame.from_catalog(database='rapid_db', table_name='rapid_inbox')
dyf.printSchema()
dyf.show()
try:
    print('Data load into Redshift started')
    redshift_load = glueContext.write_dynamic_frame.from_jdbc_conf(
    frame = dyf, 
    catalog_connection = "redshiftServerless", 
    connection_options =  {"dbtable": "public.movie_db","database": "dev"}, 
    redshift_tmp_dir = "s3://aws-glue-assets-739688330455-ap-south-1/temporary/", 
    transformation_ctx = "movie_df"
    )
    print('Data load into redshift was successful')
    dyf.show()
    print('This is the following data which was loaded into Redshift Serverless DataWareHouse')
    
except er as Exception:
    print('The following load was failed due to',er)
bucket_name='rapid-ur-s3-redshift'

print('Moving files into archive')    
os.system(f'aws s3 sync s3://{bucket_name}/inbox s3://{bucket_name}/archive')
print('file movement successfull')

job.commit()