from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator

"""
Upsert
UPSERT
MySQL -> S3 -> Redshift
"""

with DAG(
        dag_id='MySQL_to_Redshift_v2',
        catchup=False,
        schedule='0 9 * * *',
        start_date=datetime(2022, 8, 24),
        max_active_runs=1,
        default_args={
            'retries': 1,
            'retry_delay': timedelta(minutes=3),
        }
) as dags:
    schema = "gracia10"
    table = "nps"
    s3_bucket = "shee-bucket"
    s3_key = schema + "-" + table

    mysql_to_s3_nps = SqlToS3Operator(
        task_id='mysql_to_s3_nps',
        sql_conn_id="mysql_conn_id",
        aws_conn_id="aws_conn_id",
        query="SELECT * FROM prod.nps WHERE DATE(created_at) = DATE('{{ execution_date }}')",
        s3_bucket=s3_bucket,
        s3_key=s3_key,
        verify=False,
        replace=True,
        pd_kwargs={"index": False, "header": False},
    )

    s3_to_redshift_nps = S3ToRedshiftOperator(
        task_id='s3_to_redshift_nps',
        aws_conn_id="aws_conn_id",
        redshift_conn_id="redshift_dev_db",
        s3_bucket=s3_bucket,
        s3_key=s3_key,
        schema=schema,
        table=table,
        copy_options=['csv'],
        method='UPSERT',
        upsert_keys=['id']
    )

    mysql_to_s3_nps >> s3_to_redshift_nps
