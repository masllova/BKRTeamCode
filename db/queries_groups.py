import json
from datetime import datetime
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

def add_file_to_group(group_id: int, file_name: str):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE groups
            SET files = array_append(files, %s)
            WHERE id = %s;
        """, (file_name, group_id))
        conn.commit()

def add_article_to_group(group_id: int, article_name: str):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE groups
            SET articles = array_append(articles, %s)
            WHERE id = %s;
        """, (article_name, group_id))
        conn.commit()

def add_vkr_to_group(group_id: int, vkr_name: str):
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE groups
            SET vkr = array_append(vkr, %s)
            WHERE id = %s;
        """, (vkr_name, group_id))
        conn.commit()

def add_task_to_group(group_id: int, task_name: str, description: str):
    with conn.cursor() as cursor:
        cursor.execute("SELECT tasks FROM groups WHERE id = %s;", (group_id,))
        tasks = cursor.fetchone()[0] or {}
        tasks[task_name] = description
        cursor.execute("UPDATE groups SET tasks = %s WHERE id = %s;", (json.dumps(tasks), group_id))
        conn.commit()

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