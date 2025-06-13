from app.db import get_connection

# 문의글 등록 함수
def insert_inquiry(user_id, title, content, is_secret):
    """
    사용자가 작성한 문의글을 DB에 저장하는 함수
    """
    sql = """
        INSERT INTO inquiry (user_id, title, content, is_secret)
        VALUES (%s, %s, %s, %s)
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (user_id, title, content, is_secret))
        conn.commit()

# 문의글 단일 조회
def find_inquiry_by_id(inquiry_id):
    """
    문의글 ID로 단일 문의글 정보를 조회하는 함수
    """
    sql = """
        SELECT i.*, u.name
        FROM inquiry i
        JOIN user u ON i.user_id = u.id
        WHERE i.id = %s AND i.is_deleted = 0
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (inquiry_id,))
            return cursor.fetchone()

# 사용자 ID로 본인의 모든 문의글 조회
def find_inquiries_by_user(user_id):
    """
    사용자의 전체 문의글 목록을 조회하는 함수 (삭제 제외)
    """
    sql = """
        SELECT * FROM inquiry
        WHERE user_id = %s AND is_deleted = 0
        ORDER BY created_at DESC
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()

# 전체 문의글 조회 (관리자용)
def find_all_inquiries():
    """
    전체 문의글 목록을 조회하는 함수 (관리자 전용)
    """
    sql = """
        SELECT i.*, u.name
        FROM inquiry i
        JOIN user u ON i.user_id = u.id
        WHERE i.is_deleted = 0
        ORDER BY created_at DESC
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

# 문의글 수정
def update_inquiry(inquiry_id, title, content, is_secret):
    """
    제목, 내용, 비밀글 여부를 수정하는 함수
    """
    sql = """
        UPDATE inquiry
        SET title = %s,
            content = %s,
            is_secret = %s,
            updated_at = NOW()
        WHERE id = %s AND is_deleted = 0
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (title, content, is_secret, inquiry_id))
        conn.commit()

# 문의글 논리 삭제
def delete_inquiry(inquiry_id):
    """
    문의글을 논리적으로 삭제하는 함수 (is_deleted = 1)
    """
    sql = "UPDATE inquiry SET is_deleted = 1 WHERE id = %s"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (inquiry_id,))
        conn.commit()

# 조건에 맞는 문의글 목록을 검색, 정렬, 페이징하여 조회
def search_inquiries(keyword=None, page=1, size=10, sort="latest"):
    """
    조건(검색, 정렬, 페이징)에 따라 문의글 목록을 조회하는 함수
    """
    offset = (page - 1) * size
    params = []
    where_clauses = ["is_deleted = 0"]

    # 검색 조건
    if keyword:
        where_clauses.append("(title LIKE %s OR content LIKE %s)")
        like_keyword = f"%{keyword}%"
        params += [like_keyword, like_keyword]

    where_sql = " AND ".join(where_clauses)

    # 정렬 조건
    if sort == "answered":
        order_sql = "status = 'answered' DESC, created_at DESC"
    elif sort == "unanswered":
        order_sql = "status = 'open' DESC, created_at DESC"
    else:
        order_sql = "created_at DESC"  # 기본 최신순

    sql = f"""
        SELECT i.*, u.name
        FROM inquiry i
        JOIN user u ON i.user_id = u.id
        WHERE {where_sql}
        ORDER BY {order_sql}
        LIMIT %s OFFSET %s
    """

    params += [size, offset]

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
