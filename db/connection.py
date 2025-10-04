import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)
cursor = conn.cursor()