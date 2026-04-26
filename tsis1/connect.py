import psycopg2
from config import DB_CONFIG


def get_connection():
    """Returns an open connection to the database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Could not connect to the database: {e}")
        print("Check config.py — make sure host, dbname, user, and password are correct.")
        raise
