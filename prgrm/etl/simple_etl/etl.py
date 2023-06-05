import psycopg2
import requests

from prgrm.etl import credentials


def get_Redshift_connection():
    host = "learnde.cduaw970ssvt.ap-northeast-2.redshift.amazonaws.com"
    redshift_user = credentials.username
    redshift_pass = credentials.password
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
    """
    records = [
      [ "DEAN", "M" ],
      [ "Claire", "F" ],
      ...
    ]
    """
    cur = get_Redshift_connection()

    # (FULL REFRESH) DELETE FROM을 먼저 수행
    sql = "TRUNCATE TABLE gracia10.name_gender"
    cur.execute(sql)

    # INSERT 수행
    sql = "BEGIN;"
    for r in records:
        name = r[0]
        gender = r[1]
        print(name, "-", gender)
        sql += "INSERT INTO gracia10.name_gender VALUES ('{n}', '{g}');".format(n=name, g=gender)
    sql += "END;"

    cur.execute(sql)


link = "https://s3-geospatial.s3-us-west-2.amazonaws.com/name_gender.csv"

data = extract(link)
lines = transform(data)
load(lines)
