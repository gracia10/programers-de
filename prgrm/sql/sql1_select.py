import os
import psycopg2

from dotenv import load_dotenv


# .env 파일에서 환경 변수 로드
def _get_db_info() -> dict:
    load_dotenv()

    dbinfo = {'host': os.getenv("DATABASE_HOST"), 'dbname': os.getenv("DATABASE_NAME"),
              'user': os.getenv("DATABASE_USER"), 'password': os.getenv("DATABASE_PASSWORD"),
              'port': os.getenv("DATABASE_PORT")}
    return dbinfo


def _get_Redshift_connection(autocommit, host, dbname, user, password, port):
    conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password,
        port=port
    )
    conn.set_session(autocommit=autocommit)
    return conn


def main():
    dbinfo = _get_db_info()
    conn = _get_Redshift_connection(autocommit=True, **dbinfo)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM raw_data.user_session_channel limit 10")

    records = cursor.fetchall()

    for record in records:
        print(record)

    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
