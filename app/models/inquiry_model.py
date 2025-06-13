# ✅ inquiry_model.py - 리팩터링

from app.db import get_connection

# 공통 DB 유틸
def _query_one(sql, params):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

def _query_all(sql, params=None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params or ())
            return cursor.fetchall()

def _execute(sql, params):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
        conn.commit()

# 문의글 등록
def insert_inquiry(user_id, title, content, is_secret):
    sql = """
        INSERT INTO inquiry (user_id, title, content, is_secret)
        VALUES (%s, %s, %s, %s)
    """
    _execute(sql, (user_id, title, content, is_secret))

# 단일 조회
def find_inquiry_by_id(inquiry_id):
    sql = """
        SELECT i.*, u.name
        FROM inquiry i
        JOIN user u ON i.user_id = u.id
        WHERE i.id = %s AND i.is_deleted = 0
    """
    return _query_one(sql, (inquiry_id,))

# 사용자별 전체 조회
def find_inquiries_by_user(user_id):
    sql = """
        SELECT * FROM inquiry
        WHERE user_id = %s AND is_deleted = 0
        ORDER BY created_at DESC
    """
    return _query_all(sql, (user_id,))

# 관리자 전체 조회
def find_all_inquiries():
    sql = """
        SELECT i.*, u.name
        FROM inquiry i
        JOIN user u ON i.user_id = u.id
        WHERE i.is_deleted = 0
        ORDER BY created_at DESC
    """
    return _query_all(sql)

# 수정
def update_inquiry(inquiry_id, title, content, is_secret):
    sql = """
        UPDATE inquiry
        SET title = %s,
            content = %s,
            is_secret = %s,
            updated_at = NOW()
        WHERE id = %s AND is_deleted = 0
    """
    _execute(sql, (title, content, is_secret, inquiry_id))

# 논리 삭제
def delete_inquiry(inquiry_id):
    sql = "UPDATE inquiry SET is_deleted = 1 WHERE id = %s"
    _execute(sql, (inquiry_id,))

# 검색, 정렬, 페이징 조회
def search_inquiries(keyword=None, page=1, size=10, sort="latest"):
    offset = (page - 1) * size
    params = []
    where = ["i.is_deleted = 0"]

    if keyword:
        where.append("(i.title LIKE %s OR i.content LIKE %s)")
        kw = f"%{keyword}%"
        params += [kw, kw]

    where_sql = " AND ".join(where)

    if sort == "answered":
        order_sql = "i.status = 'answered' DESC, i.created_at DESC"
    elif sort == "unanswered":
        order_sql = "i.status = 'open' DESC, i.created_at DESC"
    else:
        order_sql = "i.created_at DESC"

    sql = f"""
        SELECT i.*, u.name
        FROM inquiry i
        JOIN user u ON i.user_id = u.id
        WHERE {where_sql}
        ORDER BY {order_sql}
        LIMIT %s OFFSET %s
    """
    params += [size, offset]
    return _query_all(sql, params)

# 상태 업데이트
def update_status(inquiry_id, status):
    sql = "UPDATE inquiry SET status = %s, updated_at = NOW() WHERE id = %s"
    _execute(sql, (status, inquiry_id))
