from db.connection import conn, cursor

def add_user(telegram_id: int, full_name: str, role: str, university: str, stage: str):
    cursor.execute(
        """
        INSERT INTO users (telegram_id, full_name, role, university, stage)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (telegram_id) DO NOTHING;
        """,
        (telegram_id, full_name, role, university, stage)
    )
    conn.commit()

def user_exists(telegram_id: int) -> bool:
    cursor.execute("SELECT 1 FROM users WHERE telegram_id = %s;", (telegram_id,))
    return cursor.fetchone() is not None

def get_user_role(telegram_id: int) -> str | None:
    cursor.execute(
        "SELECT role FROM users WHERE telegram_id = %s;",
        (telegram_id,)
    )
    result = cursor.fetchone()
    if result:
        return result[0]
    return None