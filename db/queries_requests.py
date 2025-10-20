from datetime import datetime
from db.connection import conn

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
            INSERT INTO requests (sender_id, receiver_id, topic, created_at)
            VALUES (%s, %s, %s, %s)
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
            SELECT r.id, r.sender_id, u.full_name AS sender_name, r.topic, r.created_at
            FROM requests r
            JOIN users u ON r.sender_id = u.id
            WHERE r.receiver_id = %s
            ORDER BY r.created_at ASC;
        """
        cursor.execute(sql, (user_id,))
        results = cursor.fetchall()

        if not results:
            return None
        return [
            {
                "id": r[0],
                "sender_id": r[1],
                "sender_name": r[2],
                "topic": r[3],
                "created_at": r[4],
            }
            for r in results
        ]

def get_outgoing_requests(user_telegram_id: int) -> list[dict] | None:
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (user_telegram_id,))
        user = cursor.fetchone()

        if not user:
            return None
        user_id = user[0]
        sql = """
            SELECT r.id, r.receiver_id, u.full_name AS receiver_name, r.topic, r.created_at
            FROM requests r
            JOIN users u ON r.receiver_id = u.id
            WHERE r.sender_id = %s
            ORDER BY r.created_at ASC;
        """
        cursor.execute(sql, (user_id,))
        results = cursor.fetchall()

        if not results:
            return None
        return [
            {
                "id": r[0],
                "receiver_id": r[1],
                "receiver_name": r[2],
                "topic": r[3],
                "created_at": r[4],
            }
            for r in results
        ]


def respond_request(request_id: int):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM requests WHERE id = %s;", (request_id,))
        conn.commit()
        print(f"Заявка {request_id} удалена.")


def request_exists(sender_telegram_id: int, receiver_telegram_id: int) -> bool:
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (sender_telegram_id,))
        sender = cursor.fetchone()

        if not sender:
            return False
        sender_id = sender[0]
        cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (receiver_telegram_id,))
        receiver = cursor.fetchone()

        if not receiver:
            return False
        receiver_id = receiver[0]
        cursor.execute(
            "SELECT 1 FROM requests WHERE sender_id = %s AND receiver_id = %s LIMIT 1;",
            (sender_id, receiver_id)
        )
        return cursor.fetchone() is not None
    
def get_request_users(request_id: int) -> tuple[int, int]:
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT sender_id, receiver_id FROM requests WHERE id = %s;",
            (request_id,)
        )
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Заявка с id {request_id} не найдена")
        return result[0], result[1]