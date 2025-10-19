from datetime import datetime
from db.connection import conn, cursor

def add_request(sender_id: int, receiver_id: int):
    cursor.execute(
        """
        INSERT INTO requests (sender_id, receiver_id, status, created_at)
        VALUES (%s, %s, 'ожидает', %s)
        RETURNING id;
        """,
        (sender_id, receiver_id, datetime.utcnow())
    )
    request_id = cursor.fetchone()[0]
    conn.commit()
    return request_id

def get_incoming_requests(user_id: int, last_id: int | None = None) -> list[dict] | None:
    sql = """
        SELECT id, sender_id, status, created_at
        FROM requests
        WHERE receiver_id = %s
    """
    params = [user_id]

    if last_id:
        sql += " AND id > %s"
        params.append(last_id)

    sql += " ORDER BY id LIMIT 3;"
    cursor.execute(sql, tuple(params))
    results = cursor.fetchall()

    if not results:
        return None

    requests = []
    for r in results:
        requests.append({
            "id": r[0],
            "sender_id": r[1],
            "status": r[2],
            "created_at": r[3],
        })
    return requests

def get_outgoing_requests(user_id: int, last_id: int | None = None) -> list[dict] | None:
    sql = """
        SELECT id, receiver_id, status, created_at
        FROM requests
        WHERE sender_id = %s
    """
    params = [user_id]

    if last_id:
        sql += " AND id > %s"
        params.append(last_id)

    sql += " ORDER BY id LIMIT 3;"
    cursor.execute(sql, tuple(params))
    results = cursor.fetchall()

    if not results:
        return None

    requests = []
    for r in results:
        requests.append({
            "id": r[0],
            "receiver_id": r[1],
            "status": r[2],
            "created_at": r[3],
        })
    return requests

def respond_request(request_id: int, accept: bool):
    status = "принято" if accept else "отклонено"
    cursor.execute(
        "UPDATE requests SET status = %s WHERE id = %s;",
        (status, request_id)
    )
    conn.commit()