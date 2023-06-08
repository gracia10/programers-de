import json
import logging
from datetime import datetime

import psycopg2
import requests
from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook


def _get_Redshift_connection(autocommit=True):
    hook = PostgresHook(postgres_conn_id='redshift_dev_db')
    conn = hook.get_conn()
    conn.autocommit = autocommit
    return conn.cursor()


def _create_table(cur, schema, table):
    cur.execute(f"DROP TABLE IF EXISTS {schema}.{table};")
    cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {schema}.{table} (
                    country varchar,
                    population varchar,
                    area varchar
                );""")


@task
def get_countries_info(url):
    logging.info(datetime.utcnow())
    res = requests.get(url)
    return json.loads(res.text)


@task
def load(schema, table, records):
    logging.info("load begin")

    cur = _get_Redshift_connection()
    try:
        cur.execute("BEGIN;")

        _create_table(cur, schema, table)

        for r in records:
            sql = f"INSERT INTO {schema}.{table} VALUES ('{r['name']['common']}', '{r['population']}', '{r['area']}');"
            logging.info(sql)
            cur.execute(sql)

        cur.execute("COMMIT;")
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        cur.execute("ROLLBACK;")
        raise

    logging.info("load done")


with DAG(
        dag_id='RestCountries',
        catchup=False,
        schedule='30 6 * * 6',
        start_date=datetime(2023, 6, 7),

) as dag:
    url = Variable.get("restcountries_url")
    schema = 'gracia10'
    table = 'restcountries'

    lines = get_countries_info(url)
    load(schema, table, lines)
