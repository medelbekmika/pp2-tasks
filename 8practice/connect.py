import psycopg2
from config import host, user, password, database

def connect_db():
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conn
