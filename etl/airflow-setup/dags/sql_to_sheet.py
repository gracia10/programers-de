from airflow import DAG
from airflow.operators.python import PythonOperator

from plugins import gsheet
from datetime import datetime


def update_gsheet(**context):
    sql = context["params"]["sql"]
    sheetfilename = context["params"]["sheetfilename"]
    sheetgid = context["params"]["sheetgid"]

    gsheet.update_sheet(sheetfilename, sheetgid, sql, "redshift_dev_db")


with DAG(
        dag_id='sql_to_sheet',
        start_date=datetime(2022, 6, 18),
        catchup=False,
        tags=['example'],
        schedule='@once'
) as dag:
    sheet_update = PythonOperator(
        dag=dag,
        task_id='update_sql_to_sheet1',
        python_callable=update_gsheet,
        params={
            "sql": "SELECT date, round as nps FROM analytics.nps_summary",
            "sheetfilename": "spreadsheet-copy-testing",
            "sheetgid": "RedshiftToSheet"
        }
    )
