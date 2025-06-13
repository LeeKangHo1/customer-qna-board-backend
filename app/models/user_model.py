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

# 사용자 논리 삭제 (is_deleted = 1)
def delete_user(user_id):
    sql = "UPDATE user SET is_deleted = 1 WHERE id = %s"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (user_id,))
        conn.commit()

# 사용자 인덱스(id) 로 검색
def find_by_id(user_id):
    sql = "SELECT * FROM user WHERE id = %s AND is_deleted = 0"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (user_id,))
            return cursor.fetchone()

# 사용자 정보 업데이트 함수 (필요한 항목만 수정)
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
        return  # 아무 필드도 없으면 업데이트 안 함

    sql = f"""
        UPDATE user
        SET {', '.join(fields)}, updated_at = NOW()
        WHERE id = %s
    """
    values.append(user_id)

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, values)
        conn.commit()
