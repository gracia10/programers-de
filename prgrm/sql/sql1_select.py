import os
import psycopg2

from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

host = os.getenv("DATABASE_HOST")
dbname = os.getenv("DATABASE_NAME")
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
port = os.getenv("DATABASE_PORT")

conn = psycopg2.connect(
    host=host,
    dbname=dbname,
    user=user,
    password=password,
    port=port
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM raw_data.user_session_channel limit 1")
records = cursor.fetchone()

for record in records:
    print(record)

cursor.close()
conn.close()
