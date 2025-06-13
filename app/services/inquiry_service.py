from app.models import inquiry_model, user_model
from flask import abort

# 문의글 작성
def create_inquiry(data):
    """사용자로부터 받은 데이터로 문의글 등록"""
    user_id = data.get("user_id")
    title = data.get("title")
    content = data.get("content")
    is_secret = data.get("is_secret", 0)

    if not user_id or not title or not content:
        return {"error": "user_id, title, content는 필수입니다."}, 400

    if not user_model.find_by_id(user_id):
        return {"error": "존재하지 않는 사용자입니다."}, 404

    inquiry_model.insert_inquiry(user_id, title, content, is_secret)
    return {"message": "문의글이 등록되었습니다."}, 201

# 단일 조회
def get_inquiry_by_id(inquiry_id):
    inquiry = inquiry_model.find_inquiry_by_id(inquiry_id)
    if not inquiry:
        return {"error": "존재하지 않는 문의글입니다."}, 404
    return inquiry, 200

# 사용자 문의글 목록 조회
def get_inquiries_by_user(user_id):
    return inquiry_model.find_inquiries_by_user(user_id), 200

# 전체 문의글 조회 (관리자)
def get_all_inquiries():
    return inquiry_model.find_all_inquiries(), 200

# 문의글 수정
def update_inquiry(inquiry_id, data):
    title = data.get("title")
    content = data.get("content")
    is_secret = data.get("is_secret", 0)

    if not title or not content:
        return {"error": "제목과 내용을 입력해주세요."}, 400

    inquiry_model.update_inquiry(inquiry_id, title, content, is_secret)
    return {"message": "문의글이 수정되었습니다."}, 200

# 문의글 삭제
def delete_inquiry(inquiry_id):
    if not inquiry_model.find_inquiry_by_id(inquiry_id):
        return {"error": "존재하지 않는 문의글입니다."}, 404

    inquiry_model.delete_inquiry(inquiry_id)
    return {"message": "문의글이 삭제되었습니다."}, 200

# 조건 기반 문의글 조회

def get_filtered_inquiries(query):
    keyword = query.get("keyword")
    try:
        page = int(query.get("page", 1))
        size = int(query.get("size", 10))
    except ValueError:
        return {"error": "page와 size는 정수여야 합니다."}, 400

    sort = query.get("sort", "latest")
    return inquiry_model.search_inquiries(keyword, page, size, sort), 200
