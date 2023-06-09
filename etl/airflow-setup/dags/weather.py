import json
import logging
from datetime import datetime

import requests
from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook

"""
8일치 날씨정보를 Increment Update
"""


def get_Redshift_connection():
    hook = PostgresHook(postgres_conn_id='redshift_dev_db')
    return hook.get_conn().cursor()


@task
def extract(link):
    res = requests.get(link)
    """
    {'dt': 1622948400, 'sunrise': 1622923873, 'sunset': 1622976631, 'moonrise': 1622915520, 'moonset': 1622962620, 'moon_phase': 0.87, 'temp': {'day': 26.59, 'min': 15.67, 'max': 28.11, 'night': 22.68, 'eve': 26.29, 'morn': 15.67}, 'feels_like': {'day': 26.59, 'night': 22.2, 'eve': 26.29, 'morn': 15.36}, 'pressure': 1003, 'humidity': 30, 'dew_point': 7.56, 'wind_speed': 4.05, 'wind_deg': 250, 'wind_gust': 9.2, 'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}], 'clouds': 44, 'pop': 0, 'uvi': 3}
    """
    return json.loads(res.text)


@task
def transform(text):
    ret = []

    for d in text["daily"]:
        day = datetime.fromtimestamp(d["dt"]).strftime('%Y-%m-%d')
        ret.append("('{}',{},{},{})".format(day, d["temp"]["day"], d["temp"]["min"], d["temp"]["max"]))

    return ret


@task
def load(schema, table, ret):
    cur = get_Redshift_connection()

    create_sql = f"""CREATE TABLE IF NOT EXISTS {schema}.{table} (
                                date date,
                                temp float,
                                min_temp float,
                                max_temp float,
                                created_date timestamp default GETDATE()
                     );
                 """
    logging.info(create_sql)

    create_temp_sql = f"CREATE TEMP TABLE t AS SELECT * FROM {schema}.{table}"
    logging.info(create_temp_sql)

    insert_temp_sql = f"INSERT INTO t VALUES " + ",".join(ret)
    logging.info(insert_temp_sql)

    alter_sql = f"""DELETE FROM {schema}.{table}; 
                    INSERT INTO {schema}.{table}
                    SELECT date, temp , min_temp , max_temp FROM (
                        SELECT *, ROW_NUMBER() OVER (PARTITION BY date ORDER BY created_date desc) as seq FROM t)
                    WHERE seq = 1;
                  """
    logging.info(alter_sql)

    try:
        cur.execute(create_sql)
        cur.execute(create_temp_sql)
        cur.execute(insert_temp_sql)
        cur.execute(alter_sql)

        cur.execute("COMMIT;")
    except Exception as e:
        cur.execute("ROLLBACK;")
        raise


with DAG(
        dag_id='weather',
        catchup=False,
        schedule='0 10 * * *',
        start_date=datetime(2023, 5, 30),
) as dags:
    lat = "37.5665"
    lon = "126.978"
    part = "Asia/Seoul"
    key = "0a1733b1c646c96dd4598999766c54c1"

    url = f"https://api.openweathermap.org/data/2.5/onecall?" \
          f"lat={lat}&lon={lon}&appid={key}&units=metric"

    schema = "gracia10"
    table = "weather_forecast"

    data = extract(url)
    ret = transform(data)
    load(schema, table, ret)
