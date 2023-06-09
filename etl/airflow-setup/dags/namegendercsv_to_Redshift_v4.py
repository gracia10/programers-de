import logging
from datetime import datetime, timedelta

import psycopg2
import requests
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

"""
개선사항
1. Connection 사용하기
"""


def get_Redshift_connection(autocommit=True):
    hook = PostgresHook(postgres_conn_id='redshift_dev_db')
    conn = hook.get_conn()
    conn.autocommit = autocommit
    return conn.cursor()


def extract(**context):
    link = context['params']["url"]
    # task_instance = context['task_instance']
    execution_date = context['execution_date']

    logging.info(execution_date)
    res = requests.get(link)
    return res.text


def transform(**context):
    logging.info("Transform started")
    text = context["task_instance"].xcom_pull(key="return_value", task_ids="extract")
    lines = text.strip().split("\n")
    records = []
    for l in lines[1:]:
        (name, gender) = l.split(",")  # l = "DEAN,M" -> [ 'DEAN', 'M' ]
        records.append([name, gender])

    logging.info("Transform ended")
    return records


def load(**context):
    logging.info("load started")
    schema = context["params"]["schema"]
    table = context["params"]["table"]

    records = context["task_instance"].xcom_pull(key="return_value", task_ids="transform")

    cur = get_Redshift_connection()
    try:
        cur.execute("BEGIN;")

        # (FULL REFRESH) DELETE FROM을 먼저 수행
        sql = f"DELETE FROM {schema}.{table};"
        cur.execute(sql)

        # INSERT 수행
        for r in records:
            name = r[0]
            gender = r[1]
            print(name, "-", gender)
            sql = f"INSERT INTO {schema}.{table} VALUES ('{name}', '{gender}');"
            cur.execute(sql)
        cur.execute("END;")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK;")
        raise

    logging.info("load done")


dag = DAG(
    dag_id='name_gender_v4',
    catchup=False,
    start_date=datetime(2023, 4, 6),
    schedule='0 2 * * *',
    default_args={
        'retries': 1,
        'retry_delay': timedelta(minutes=3),
    }
)

extract = PythonOperator(
    task_id='extract',
    python_callable=extract,
    params={
        'url': Variable.get("csv_url")
    },
    dag=dag,
)

transform = PythonOperator(
    task_id='transform',
    python_callable=transform,
    dag=dag,
)

load = PythonOperator(
    task_id='load',
    python_callable=load,
    params={
        'schema': 'gracia10',
        'table': 'name_gender'
    },
    dag=dag,
)

extract >> transform >> load
