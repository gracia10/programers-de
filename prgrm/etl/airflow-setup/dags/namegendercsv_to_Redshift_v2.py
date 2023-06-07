import logging
from datetime import datetime, timedelta

import psycopg2
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator

"""
개선사항
1. params를 통해 변수 넘기기
2. execution_date 얻어내기
"""


def get_Redshift_connection():
    host = "learnde.cduaw970ssvt.ap-northeast-2.redshift.amazonaws.com"
    redshift_user = ''
    redshift_pass = ''
    port = 5439
    dbname = "dev"
    conn = psycopg2.connect("dbname={dbname} user={user} host={host} password={password} port={port}".format(
        dbname=dbname,
        user=redshift_user,
        password=redshift_pass,
        host=host,
        port=port
    ))
    conn.set_session(autocommit=True)
    return conn.cursor()


def extract(url):
    res = requests.get(url)
    return res.text


def transform(text):
    lines = text.strip().split("\n")
    records = []
    for l in lines[1:]:
        (name, gender) = l.split(",")  # l = "DEAN,M" -> [ 'DEAN', 'M' ]
        records.append([name, gender])
    return records


def load(records):
    cur = get_Redshift_connection()

    try:
        cur.execute("BEGIN;")

        # (FULL REFRESH) DELETE FROM을 먼저 수행
        sql = "DELETE FROM gracia10.name_gender;"
        cur.execute(sql)

        # INSERT 수행
        for r in records:
            name = r[0]
            gender = r[1]
            print(name, "-", gender)
            sql = "INSERT INTO gracia10.name_gender VALUES ('{n}', '{g}');".format(n=name, g=gender)
            cur.execute(sql)
        cur.execute("END;")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK;")
        raise


def etl(**context):
    link = context['params']["url"]
    # task_instance = context['task_instance']
    execution_date = context['execution_date']

    logging.info(execution_date)

    data = extract(link)
    lines = transform(data)
    load(lines)


dag_second_assignment = DAG(
    dag_id='name_gender_v2',
    catchup=False,
    start_date=datetime(2023, 4, 6),
    schedule='0 2 * * *',
    default_args={
        'retries': 1,
        'retry_delay': timedelta(minutes=3),
    }
)

task = PythonOperator(
    task_id='perform_etl',
    python_callable=etl,
    dag=dag_second_assignment,
    params={
        'url': "https://s3-geospatial.s3-us-west-2.amazonaws.com/name_gender.csv"
    }
)
