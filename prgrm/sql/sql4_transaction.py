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
    conn = _get_Redshift_connection(autocommit=False, **dbinfo)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM adhoc.keeyong_name_gender")
        cursor.execute("INSERT INTO adhoc.keeyong_name_gender VALUES ('Claire1','Female');")
        cursor.execute("INSERT INTO adhoc.keeyong_name_gender VALUES ('Claire2','Female');")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    main()
