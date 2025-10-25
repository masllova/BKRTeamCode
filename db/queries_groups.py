import json
import os
import uuid
from datetime import datetime
from datetime import date
from db.connection import conn

def get_group_by_id(group_id: int) -> dict | None:
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM groups
            WHERE id = %s;
        """, (group_id,))
        result = cursor.fetchone()
        if not result:
            return None
        keys = [desc[0] for desc in cursor.description]
        return dict(zip(keys, result))

def create_group(teacher_id: int, student_id: int, name: str) -> int:
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO groups (teacher_id, student_id, name, tasks, deadlines, files, created_at, articles, vkr)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (teacher_id, student_id, name, json.dumps({}), json.dumps({}), [], datetime.now(), [], [])
        )
        group_id = cursor.fetchone()[0]
        conn.commit()
        return group_id

def update_group_name(group_id: int, new_name: str):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE groups
            SET name = %s
            WHERE id = %s;
        """, (new_name, group_id))
        conn.commit()

def delete_group(group_id: int):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM groups WHERE id = %s;", (group_id,))
        conn.commit()

def add_file_to_group(group_id: int, value: str, kind: str = "file"):
    """
    value: путь к файлу или ссылка
    kind: 'file' или 'link'
    """
    if kind not in ("file", "link"):
        raise ValueError("Неверный тип элемента")
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT files FROM groups WHERE id = %s", (group_id,))
        current = cursor.fetchone()[0] or []

        if kind == "file":
            filename = os.path.basename(value)
            base, ext = os.path.splitext(filename)
            counter = 1
            existing_names = [os.path.basename(item["value"]) for item in current if item["type"] == "file"]
            new_filename = filename
            while new_filename in existing_names:
                new_filename = f"{base}{counter}{ext}"
                counter += 1
            value = os.path.join(os.path.dirname(value), new_filename)

        new_item = {"type": kind, "value": value}
        current.append(new_item)
        cursor.execute("UPDATE groups SET files = %s WHERE id = %s", (json.dumps(current), group_id))
        conn.commit()


def add_article_to_group(group_id: int, value: str, kind: str = "file"):
    """
    value: путь к файлу или ссылка
    kind: 'file' или 'link'
    """
    if kind not in ("file", "link"):
        raise ValueError("Неверный тип элемента")
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT articles FROM groups WHERE id = %s", (group_id,))
        current = cursor.fetchone()[0] or []

        if kind == "file":
            filename = os.path.basename(value)
            base, ext = os.path.splitext(filename)
            counter = 1
            existing_names = [os.path.basename(item["value"]) for item in current if item["type"] == "file"]
            new_filename = filename
            while new_filename in existing_names:
                new_filename = f"{base}{counter}{ext}"
                counter += 1
            value = os.path.join(os.path.dirname(value), new_filename)

        new_item = {"type": kind, "value": value}
        current.append(new_item)
        cursor.execute("UPDATE groups SET articles = %s WHERE id = %s", (json.dumps(current), group_id))
        conn.commit()

def add_vkr_to_group(group_id: int, value: str, kind: str = "file"):
    """
    value: путь к файлу или ссылка
    kind: 'file' или 'link'
    Перезаписывает поле vkr целиком, но если файл с таким именем уже есть, добавляет суффикс
    """
    if kind not in ("file", "link"):
        raise ValueError("Неверный тип элемента")
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT vkr FROM groups WHERE id = %s", (group_id,))
        current = cursor.fetchone()[0] or []
        if kind == "file":
            filename = os.path.basename(value)
            base, ext = os.path.splitext(filename)
            counter = 1

            existing_names = [os.path.basename(item["value"]) for item in current if item["type"] == "file"]
            new_filename = filename
            while new_filename in existing_names:
                new_filename = f"{base}{counter}{ext}"
                counter += 1

            value = os.path.join(os.path.dirname(value), new_filename)
        
        new_item = {"type": kind, "value": value}
        cursor.execute("UPDATE groups SET vkr = %s WHERE id = %s", (json.dumps([new_item]), group_id))
        conn.commit()

def add_task_to_group(group_id: int, task_name: str):
    task_id = str(uuid.uuid4())
    new_task = {
        "name": task_name,
        "done": False,
        "created_at": date.today().isoformat()
    }

    with conn.cursor() as cursor:
        cursor.execute("SELECT tasks FROM groups WHERE id = %s;", (group_id,))
        row = cursor.fetchone()
        tasks = row[0] or {}

        if isinstance(tasks, str):
            tasks = json.loads(tasks)

        tasks[task_id] = new_task
        cursor.execute(
            "UPDATE groups SET tasks = %s WHERE id = %s;",
            (json.dumps(tasks), group_id)
        )
        conn.commit()
    return task_id

def set_task_status(group_id: int, task_id: str, done: bool):
    with conn.cursor() as cursor:
        cursor.execute("SELECT tasks FROM groups WHERE id = %s;", (group_id,))
        row = cursor.fetchone()

        if not row or not row[0]:
            return False
        tasks = row[0]

        if isinstance(tasks, str):
            tasks = json.loads(tasks)
        if task_id not in tasks:
            return False
        tasks[task_id]["done"] = done
        cursor.execute(
            "UPDATE groups SET tasks = %s WHERE id = %s;",
            (json.dumps(tasks), group_id)
        )
        conn.commit()
    return True

def delete_task_from_group(group_id: int, task_name: str):
    with conn.cursor() as cursor:
        cursor.execute("SELECT tasks FROM groups WHERE id = %s;", (group_id,))
        tasks = cursor.fetchone()[0] or {}
        if task_name in tasks:
            tasks.pop(task_name)
            cursor.execute("UPDATE groups SET tasks = %s WHERE id = %s;", (json.dumps(tasks), group_id))
            conn.commit()

def add_deadline_to_group(group_id: int, task_name: str, deadline: str):
    with conn.cursor() as cursor:
        cursor.execute("SELECT deadlines FROM groups WHERE id = %s;", (group_id,))
        deadlines = cursor.fetchone()[0] or {}
        deadlines[task_name] = deadline
        cursor.execute("UPDATE groups SET deadlines = %s WHERE id = %s;", (json.dumps(deadlines), group_id))
        conn.commit()

def delete_deadline_from_group(group_id: int, task_name: str):
    with conn.cursor() as cursor:
        cursor.execute("SELECT deadlines FROM groups WHERE id = %s;", (group_id,))
        deadlines = cursor.fetchone()[0] or {}
        if task_name in deadlines:
            deadlines.pop(task_name)
            cursor.execute("UPDATE groups SET deadlines = %s WHERE id = %s;", (json.dumps(deadlines), group_id))
            conn.commit()