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

def add_group_to_user(user_id: int, group_id: int):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE users
            SET group_ids = array_append(group_ids, %s)
            WHERE id = %s;
        """, (group_id, user_id))
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

def get_user_by_chat_id(telegram_id: int) -> dict | None:
    cursor.execute(
        "SELECT telegram_id, full_name, role, university, stage FROM users WHERE telegram_id = %s;",
        (telegram_id,)
    )
    result = cursor.fetchone()
    if result:
        return {
            "telegram_id": result[0],
            "full_name": result[1],
            "role": result[2],
            "university": result[3],
            "stage": result[4],
        }
    return None

def get_user_by_id(user_id: int) -> dict | None:
    cursor.execute(
        "SELECT telegram_id, full_name, role, university, stage FROM users WHERE id = %s;",
        (user_id,)
    )
    result = cursor.fetchone()
    if result:
        return {
            "telegram_id": result[0],
            "full_name": result[1],
            "role": result[2],
            "university": result[3],
            "stage": result[4],
        }
    return None

def search_users(query: str, target_role: str, last_id: int | None = None) -> list[dict] | None:
    base_sql = """
        SELECT id, telegram_id, full_name, role, university, stage, faculty, department, articles, research_interests
        FROM users
        WHERE role = %s
    """
    params = [target_role]

    if last_id:
        base_sql += " AND id > %s"
        params.append(last_id)

    base_sql += """
      AND (
           full_name ILIKE %s
        OR university ILIKE %s
        OR stage ILIKE %s
        OR faculty ILIKE %s
        OR department ILIKE %s
        OR articles ILIKE %s
        OR research_interests ILIKE %s
      )
    ORDER BY id
    LIMIT 3;
    """

    search_pattern = f"%{query}%"
    params.extend([search_pattern] * 7)
    cursor.execute(base_sql, tuple(params))
    results = cursor.fetchall()

    if not results:
        return None

    users = []
    for r in results:
        users.append({
            "id": r[0],
            "telegram_id": r[1],
            "full_name": r[2],
            "role": r[3],
            "university": r[4],
            "stage": r[5],
            "faculty": r[6],
            "department": r[7],
            "articles": r[8],
            "research_interests": r[9],
        })

    return users