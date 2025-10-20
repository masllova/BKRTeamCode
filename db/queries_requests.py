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

def get_incoming_requests(user_telegram_id: int) -> list[dict] | None:
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (user_telegram_id,))
        user = cursor.fetchone()

        if not user:
            return None
        user_id = user[0]

        sql = """
            SELECT r.id, r.sender_id, u.full_name AS sender_name, r.topic, r.status, r.created_at
            FROM requests r
            JOIN users u ON r.sender_id = u.id
            WHERE r.receiver_id = %s
            ORDER BY r.created_at ASC;
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
                "sender_name": r[2],
                "topic": r[3],
                "status": r[4],
                "created_at": r[5],
            })
        return requests


def get_outgoing_requests(user_telegram_id: int) -> list[dict] | None:
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (user_telegram_id,))
        user = cursor.fetchone()
        
        if not user:
            return None
        user_id = user[0]

        sql = """
            SELECT r.id, r.receiver_id, u.full_name AS receiver_name, r.topic, r.status, r.created_at
            FROM requests r
            JOIN users u ON r.receiver_id = u.id
            WHERE r.sender_id = %s
            ORDER BY r.created_at ASC;
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
                "receiver_name": r[2],
                "topic": r[3],
                "status": r[4],
                "created_at": r[5],
            })
        return requests


def respond_request(request_id: int, accept: bool):
    status = "принято" if accept else "отклонено"
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE requests SET status = %s WHERE id = %s;",
            (status, request_id)
        )
        conn.commit()
        print(f"✔️ Заявка {request_id} обновлена: {status}")