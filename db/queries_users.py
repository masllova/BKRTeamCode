from db.connection import conn, cursor

def add_user(telegram_id: int, full_name: str, role: str = "студент"):
    cursor.execute(
        """
        INSERT INTO users (telegram_id, full_name, role)
        VALUES (%s, %s, %s)
        ON CONFLICT (telegram_id) DO NOTHING;
        """,
        (telegram_id, full_name, role)
    )
    conn.commit()

def user_exists(telegram_id: int) -> bool:
    cursor.execute("SELECT 1 FROM users WHERE telegram_id = %s;", (telegram_id,))
    return cursor.fetchone() is not None