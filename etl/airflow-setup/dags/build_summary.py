import os
from datetime import datetime, timedelta
from plugins import redshift_summary
from plugins import slack
from airflow import DAG

dag = DAG(
    dag_id="build_summary",
    schedule="25 13 * * *",
    start_date=datetime(2021, 9, 17),
    catchup=False,
    max_active_runs=1,
    concurrency=1,
    default_args={
        'on_failure_callback': slack.on_failure_callback,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
    }
)

# this should be listed in dependency order (all in analytics)
tables_load = [
    'nps_summary',
    'mau_summary',
    'channel_summary'
]

dag_root_path = os.path.dirname(os.path.abspath(__file__))
redshift_summary.build_summary_table(dag_root_path, dag, tables_load, "redshift_dev_db")
