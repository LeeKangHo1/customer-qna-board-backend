# ✅ answer_model.py - 리팩터링

from app.db import get_connection

# 공통 DB 실행 함수 (단일/다중)
def _fetch(sql, params=(), one=False):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone() if one else cursor.fetchall()

def _execute(sql, params):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
        conn.commit()

# 답변 등록
def insert_answer(inquiry_id, admin_id, content):
    sql = """
        INSERT INTO answer (inquiry_id, admin_id, content)
        VALUES (%s, %s, %s)
    """
    _execute(sql, (inquiry_id, admin_id, content))

# 답변 단일 조회
def find_answer_by_id(answer_id):
    sql = """
        SELECT a.*, u.name AS admin_name
        FROM answer a
        JOIN user u ON a.admin_id = u.id
        WHERE a.id = %s AND a.is_deleted = 0
    """
    return _fetch(sql, (answer_id,), one=True)

# 특정 문의글의 답변 목록 조회
def find_answers_by_inquiry(inquiry_id):
    sql = """
        SELECT a.*, u.name AS admin_name
        FROM answer a
        JOIN user u ON a.admin_id = u.id
        WHERE a.inquiry_id = %s AND a.is_deleted = 0
        ORDER BY a.created_at ASC
    """
    return _fetch(sql, (inquiry_id,))

# 답변 수정
def update_answer(answer_id, content):
    sql = """
        UPDATE answer
        SET content = %s,
            updated_at = NOW()
        WHERE id = %s AND is_deleted = 0
    """
    _execute(sql, (content, answer_id))

# 답변 삭제 (논리 삭제)
def delete_answer(answer_id):
    sql = "UPDATE answer SET is_deleted = 1 WHERE id = %s"
    _execute(sql, (answer_id,))
