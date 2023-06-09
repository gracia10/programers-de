import logging
from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
import yfinance as yf

"""
애플 주식 Full Refresh
"""


def get_Redshift_connection(autocommit=True):
    hook = PostgresHook(postgres_conn_id='redshift_dev_db')
    conn = hook.get_conn()
    conn.autocommit = autocommit
    return conn.cursor()


@task
def get_historical_prices(symbol):
    ticket = yf.Ticker(symbol)
    data = ticket.history()
    records = []

    for index, row in data.iterrows():
        date = index.strftime('%Y-%m-%d %H:%M:%S')

        records.append([date, row["Open"], row["High"], row["Low"], row["Close"], row["Volume"]])

    return records


@task
def load(schema, table, records):
    logging.info("load started")
    cur = get_Redshift_connection()
    try:
        cur.execute("BEGIN;")
        cur.execute(f"DROP TABLE IF EXISTS {schema}.{table};")
        cur.execute(f"""
                    CREATE TABLE {schema}.{table} (
                        date date,
                        "open" float,
                        high float,
                        low float,
                        close float,
                        volume bigint
                    );""")
        # DELETE FROM을 먼저 수행 -> FULL REFRESH을 하는 형태
        for r in records:
            sql = f"INSERT INTO {schema}.{table} VALUES ('{r[0]}', {r[1]}, {r[2]}, {r[3]}, {r[4]}, {r[5]});"
            print(sql)
            cur.execute(sql)
        cur.execute("COMMIT;")  # cur.execute("END;")
    except Exception as error:
        print(error)
        cur.execute("ROLLBACK;")
        raise

    logging.info("load done")


with DAG(
        dag_id='UpdateSymbol_v1',
        start_date=datetime(2023, 5, 30),
        catchup=False,
        schedule='0 10 * * *',
        tags=['API'],
) as dag:
    results = get_historical_prices("AAPL")
    load("gracia10", "stock_info", results)
