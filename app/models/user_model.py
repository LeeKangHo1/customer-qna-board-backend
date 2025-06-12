from app.db import get_connection

# login_id로 사용자 조회
def find_by_login_id(login_id):
    sql = "SELECT * FROM user WHERE login_id = %s AND is_deleted = 0"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (login_id,))
            return cursor.fetchone()

# email로 사용자 조회
def find_by_email(email):
    sql = "SELECT * FROM user WHERE email = %s AND is_deleted = 0"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (email,))
            return cursor.fetchone()

# 사용자 삽입
def insert_user(login_id, hashed_pw, name, email):
    sql = """
        INSERT INTO user (login_id, password, name, email)
        VALUES (%s, %s, %s, %s)
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (login_id, hashed_pw, name, email))
        conn.commit()
