import logging
from datetime import datetime, timedelta

import psycopg2
import requests
from airflow import DAG
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task

"""
개선사항
1. from airflow.decorators import task
2. Slack 
"""


def get_Redshift_connection(autocommit=True):
    hook = PostgresHook(postgres_conn_id='redshift_dev_db')
    conn = hook.get_conn()
    conn.autocommit = autocommit
    return conn.cursor()


@task
def extract(url):
    logging.info(datetime.utcnow())
    res = requests.get(url)
    return res.text


@task
def transform(text):
    logging.info("Transform started")
    lines = text.strip().split("\n")
    records = []
    for l in lines[1:]:
        (name, gender) = l.split(",")  # l = "DEAN,M" -> [ 'DEAN', 'M' ]
        records.append([name, gender])

    logging.info("Transform ended")
    return records


@task
def load(schema, table, records):
    logging.info("load started")

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


with DAG(
        dag_id='name_gender_v5',
        catchup=False,
        start_date=datetime(2023, 4, 6),
        schedule='0 2 * * *',
        default_args={
            'retries': 1,
            'retry_delay': timedelta(minutes=3),
            # 'on_failure_callback': slack.on_failure_callback,
        }
) as dag:
    url = Variable.get("csv_url")
    schema = 'gracia10'
    table = 'name_gender'

    lines = transform(extract(url))
    load(schema, table, lines)
