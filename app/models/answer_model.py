from app.db import get_connection

# 답변 등록
def insert_answer(inquiry_id, admin_id, content):
    """
    답변을 DB에 삽입하는 함수
    """
    sql = """
        INSERT INTO answer (inquiry_id, admin_id, content)
        VALUES (%s, %s, %s)
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (inquiry_id, admin_id, content))
        conn.commit()


# 답변 단일 조회
def find_answer_by_id(answer_id):
    """
    답변 ID로 단일 답변 조회
    """
    sql = """
        SELECT a.*, u.name AS admin_name
        FROM answer a
        JOIN user u ON a.admin_id = u.id
        WHERE a.id = %s AND a.is_deleted = 0
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (answer_id,))
            return cursor.fetchone()


# 특정 문의글의 답변 목록 조회
def find_answers_by_inquiry(inquiry_id):
    """
    inquiry_id에 해당하는 모든 답변 조회
    """
    sql = """
        SELECT a.*, u.name AS admin_name
        FROM answer a
        JOIN user u ON a.admin_id = u.id
        WHERE a.inquiry_id = %s AND a.is_deleted = 0
        ORDER BY a.created_at ASC
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (inquiry_id,))
            return cursor.fetchall()


# 답변 수정
def update_answer(answer_id, content):
    """
    답변 내용을 수정하는 함수
    """
    sql = """
        UPDATE answer
        SET content = %s,
            updated_at = NOW()
        WHERE id = %s AND is_deleted = 0
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (content, answer_id))
        conn.commit()


# 답변 삭제 (논리 삭제)
def delete_answer(answer_id):
    """
    답변을 논리적으로 삭제하는 함수 (is_deleted = 1)
    """
    sql = "UPDATE answer SET is_deleted = 1 WHERE id = %s"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (answer_id,))
        conn.commit()
