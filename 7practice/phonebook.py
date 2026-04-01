import psycopg2

conn = psycopg2.connect(
    dbname="phonebook_db",
    user="meruertmedelbek",
    password="",
    host="localhost",
    port="5432"
)

cur = conn.cursor()



#2
from connect import connect
conn = connect()
if conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook;")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()
