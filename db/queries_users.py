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

def get_user_group_ids(telegram_id: int) -> list[int]:
    with conn.cursor() as cursor:
        cursor.execute("SELECT group_ids FROM users WHERE telegram_id = %s;", (telegram_id,))
        result = cursor.fetchone()
        if not result or not result[0]:
            return []
        return result[0]

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
    cursor.execute("""
        SELECT id, telegram_id, full_name, role, created_at, university, stage,
               faculty, department, articles, research_interests, group_ids,
               degree, email, specialty
        FROM users
        WHERE telegram_id = %s;
    """, (telegram_id,))
    
    result = cursor.fetchone()
    if result:
        return {
            "id": result[0],
            "telegram_id": result[1],
            "full_name": result[2],
            "role": result[3],
            "created_at": result[4],
            "university": result[5],
            "stage": result[6],
            "faculty": result[7],
            "department": result[8],
            "articles": result[9],
            "research_interests": result[10],
            "group_ids": result[11],
            "degree": result[12],
            "email": result[13],
            "specialty": result[14],
        }
    return None

def update_user_info(telegram_id: int, field_name: str, value: str):
    """Обновляет одно строковое поле пользователя по telegram_id."""
    allowed_fields = {
        "university",
        "stage",
        "faculty",
        "department",
        "articles",
        "research_interests",
        "degree",
        "email",
        "specialty",
    }

    if field_name not in allowed_fields:
        raise ValueError(f"Поле '{field_name}' недопустимо для обновления")

    query = f"UPDATE users SET {field_name} = %s WHERE telegram_id = %s;"

    with conn.cursor() as cursor:
        cursor.execute(query, (value, telegram_id))
        conn.commit()

def get_user_by_id(user_id: int) -> dict | None:
    cursor.execute("""
        SELECT telegram_id, full_name, role, university, stage, email
        FROM users
        WHERE id = %s;
    """, (user_id,))
    
    result = cursor.fetchone()
    if result:
        return {
            "telegram_id": result[0],
            "full_name": result[1],
            "role": result[2],
            "university": result[3],
            "stage": result[4],
            "email": result[5],
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