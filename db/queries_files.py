import psycopg2
from db.connection import conn

def add_file(file_bytes: bytes) -> int:
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO files (data)
            VALUES (%s)
            RETURNING id
        """, (psycopg2.Binary(file_bytes),))
        file_id = cursor.fetchone()[0]
        conn.commit()
        return file_id
    
def get_file(file_path: str) -> bytes | None:
    """
    Читает файл с диска по пути и возвращает байты.
    """
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None
    