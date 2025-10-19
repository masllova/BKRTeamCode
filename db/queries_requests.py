from datetime import datetime
from db.connection import conn, cursor

def add_request(sender_telegram_id: int, receiver_telegram_id: int, topic: str):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (sender_telegram_id,))
        sender = cursor.fetchone()
        if not sender:
            raise ValueError(f"Sender with telegram_id {sender_telegram_id} not found")
        sender_id = sender[0]

        cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (receiver_telegram_id,))
        receiver = cursor.fetchone()
        if not receiver:
            raise ValueError(f"Receiver with telegram_id {receiver_telegram_id} not found")
        receiver_id = receiver[0]

        cursor.execute(
            """
            INSERT INTO requests (sender_id, receiver_id, status, topic, created_at)
            VALUES (%s, %s, 'ожидает', %s, %s)
            RETURNING id;
            """,
            (sender_id, receiver_id, topic, datetime.utcnow())
        )
        request_id = cursor.fetchone()[0]
        conn.commit()
        print(f"✔️ Заявка создана, id: {request_id}")

def get_incoming_requests(user_id: int) -> list[dict] | None:
    sql = """
        SELECT id, sender_id, topic, status, created_at
        FROM requests
        WHERE receiver_id = %s
        ORDER BY created_at ASC;
    """
    cursor.execute(sql, (user_id,))
    results = cursor.fetchall()

    if not results:
        return None

    requests = []
    for r in results:
        requests.append({
            "id": r[0],
            "sender_id": r[1],
            "topic": r[2],
            "status": r[3],
            "created_at": r[4],
        })
    return requests

def get_outgoing_requests(user_id: int) -> list[dict] | None:
    sql = """
        SELECT id, receiver_id, topic, status, created_at
        FROM requests
        WHERE sender_id = %s
        ORDER BY created_at ASC;
    """
    cursor.execute(sql, (user_id,))
    results = cursor.fetchall()

    if not results:
        return None

    requests = []
    for r in results:
        requests.append({
            "id": r[0],
            "receiver_id": r[1],
            "topic": r[2],
            "status": r[3],
            "created_at": r[4],
        })
    return requests

def respond_request(request_id: int, accept: bool):
    status = "принято" if accept else "отклонено"
    cursor.execute(
        "UPDATE requests SET status = %s WHERE id = %s;",
        (status, request_id)
    )
    conn.commit()