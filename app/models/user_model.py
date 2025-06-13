# ✅ user_model.py - 리팩터링 제안

from app.db import get_connection

def _query_one(sql, params):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

def _execute(sql, params):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
        conn.commit()

def find_by_login_id(login_id):
    return _query_one("SELECT * FROM user WHERE login_id = %s AND is_deleted = 0", (login_id,))

def find_by_email(email):
    return _query_one("SELECT * FROM user WHERE email = %s AND is_deleted = 0", (email,))

def insert_user(login_id, hashed_pw, name, email):
    sql = """
        INSERT INTO user (login_id, password, name, email)
        VALUES (%s, %s, %s, %s)
    """
    _execute(sql, (login_id, hashed_pw, name, email))

def delete_user(user_id):
    _execute("UPDATE user SET is_deleted = 1 WHERE id = %s", (user_id,))

def find_by_id(user_id):
    return _query_one("SELECT * FROM user WHERE id = %s AND is_deleted = 0", (user_id,))

def update_user(user_id, name=None, email=None, hashed_pw=None):
    fields = []
    values = []
    if name:
        fields.append("name = %s")
        values.append(name)
    if email:
        fields.append("email = %s")
        values.append(email)
    if hashed_pw:
        fields.append("password = %s")
        values.append(hashed_pw)
    if not fields:
        return
    fields.append("updated_at = NOW()")
    values.append(user_id)
    sql = f"UPDATE user SET {', '.join(fields)} WHERE id = %s"
    _execute(sql, tuple(values))
