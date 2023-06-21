import os
from datetime import datetime, timedelta

from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator

from plugins import slack, gsheet, s3
from airflow import DAG

"""
 - 구글 스프레드시트에서 읽기를 쉽게 해주는 모듈입니다. 아직은 쓰는 기능은 없습니다만 쉽게 추가 가능합니다.

 - 메인 함수는 get_google_sheet_to_csv입니다.
  - 이는 google sheet API를 통해 구글 스프레드시트를 읽고 쓰는 것이 가능하게 해줍니다.

 - 아래 2개의 모듈 설치가 별도로 필요합니다.
  - pip3 install oauth2client
  - pip3 install gspread

 - get_google_sheet_to_csv 함수:
  - 첫 번째 인자로 스프레드시트 링크를 제공. 이 시트를 service account 이메일과 공유해야합니다.
  - 두 번째 인자로 데이터를 읽어올 tab의 이름을 지정합니다.
  - 세 번째 인자로 지정된 test.csv로 저장합니다.
    gsheet.get_google_sheet_to_csv(
        'https://docs.google.com/spreadsheets/d/1hW-_16OqgctX-_lXBa0VSmQAs98uUnmfOqvDYYjuE50/',
        'Test',
        'test.csv',
    )

 - 여기 예제에서는 아래와 같이 테이블을 만들어두고 이를 구글스프레드시트로부터 채운다
CREATE TABLE keeyong.spreadsheet_copy_testing (
    col1 int,
    col2 int,
    col3 int,
    col4 int
);
"""


def download_tab_in_gsheet(**context):
    url = context["params"]["url"]
    tab = context["params"]["tab"]
    table = context["params"]["table"]
    data_dir = Variable.get("DATA_DIR") + "/"

    gsheet.get_google_sheet_to_csv(
        url,
        tab,
        data_dir + '{}.csv'.format(table)
    )


def copy_to_s3(**context):
    table = context["params"]["table"]
    s3_key = context["params"]["s3_key"]

    s3_conn_id = "aws_conn_id"
    s3_bucket = "grepp-data-engineering"
    data_dir = Variable.get("DATA_DIR") + "/"
    local_files_to_upload = [data_dir + '{}.csv'.format(table)]
    replace = True

    s3.upload_to_s3(s3_conn_id, s3_bucket, s3_key, local_files_to_upload, replace)


dag = DAG(
    dag_id="gsheet_to_redshift",
    start_date=datetime(2021, 9, 17),
    schedule="25 13 * * *",
    catchup=False,
    max_active_runs=1,
    max_active_tasks=2,
    default_args={
        'on_failure_callback': slack.on_failure_callback,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
    }
)

sheets = [
    {
        "url": "https://docs.google.com/spreadsheets/d/1Pn-Dbrf17LxmeCAR27Pw3Ozvr8ru-KFSjAgD2HM-OK4/edit?usp=sharing",
        "tab": "SheetToRedshift",
        "schema": "gracia10",
        "table": "spreadsheet_copy_testing"
    }
]

for sheet in sheets:
    download_tab_in_gsheet = PythonOperator(
        task_id='download_{}_in_gsheet'.format(sheet["table"]),
        python_callable=download_tab_in_gsheet,
        params=sheet,
        dag=dag)

    s3_key = sheet["schema"] + "_" + sheet["table"]

    copy_to_s3 = PythonOperator(
        task_id='copy_{}_to_s3'.format(sheet["table"]),
        python_callable=copy_to_s3,
        params={
            "table": sheet["table"],
            "s3_key": s3_key
        },
        dag=dag)

    run_copy_sql = S3ToRedshiftOperator(
        task_id='run_copy_sql_{}'.format(sheet["table"]),
        s3_bucket="grepp-data-engineering",
        s3_key=s3_key,
        schema=sheet["schema"],
        table=sheet["table"],
        copy_options=['csv', 'IGNOREHEADER 1'],
        method='REPLACE',
        redshift_conn_id="redshift_dev_db",
        aws_conn_id='aws_conn_id'.upper(),
        dag=dag
    )

    download_tab_in_gsheet >> copy_to_s3 >> run_copy_sql
