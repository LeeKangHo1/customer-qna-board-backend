from app.models import inquiry_model, user_model
from flask import abort

# 문의글을 작성하는 함수
def create_inquiry(data):
    """
    제목, 내용, 비밀글 여부를 받아 새 문의글을 생성하는 함수
    """
    user_id = data.get("user_id")
    title = data.get("title")
    content = data.get("content")
    is_secret = data.get("is_secret", 0)

    if not user_id or not title or not content:
        return {"error": "user_id, title, content는 필수입니다."}, 400

    # 사용자 존재 여부 확인
    user = user_model.find_by_id(user_id)
    if not user:
        return {"error": "존재하지 않는 사용자입니다."}, 404

    inquiry_model.insert_inquiry(user_id, title, content, is_secret)

    return {"message": "문의글이 등록되었습니다."}, 201


# 문의글 단일 조회 함수
def get_inquiry_by_id(inquiry_id):
    """
    inquiry_id로 문의글을 조회하고 없거나 삭제된 경우 처리
    """
    inquiry = inquiry_model.find_inquiry_by_id(inquiry_id)
    if not inquiry:
        return {"error": "존재하지 않는 문의글입니다."}, 404
    return inquiry, 200


# 사용자 ID로 자신의 문의글 목록을 조회하는 함수
def get_inquiries_by_user(user_id):
    """
    사용자 ID로 작성한 모든 문의글 목록을 조회하는 함수
    """
    return inquiry_model.find_inquiries_by_user(user_id), 200


# 전체 문의글 목록을 조회하는 함수 (관리자 용)
def get_all_inquiries():
    """
    관리자 전용 전체 문의글 목록 조회
    """
    return inquiry_model.find_all_inquiries(), 200


# 문의글 수정 함수
def update_inquiry(inquiry_id, data):
    """
    inquiry_id로 문의글을 수정하는 함수
    """
    title = data.get("title")
    content = data.get("content")
    is_secret = data.get("is_secret", 0)

    if not title or not content:
        return {"error": "제목과 내용을 입력해주세요."}, 400

    inquiry_model.update_inquiry(inquiry_id, title, content, is_secret)

    return {"message": "문의글이 수정되었습니다."}, 200


# 문의글 삭제 함수 (논리 삭제)
def delete_inquiry(inquiry_id):
    """
    inquiry_id로 문의글을 논리 삭제하는 함수
    """
    inquiry = inquiry_model.find_inquiry_by_id(inquiry_id)
    if not inquiry:
        return {"error": "존재하지 않는 문의글입니다."}, 404

    inquiry_model.delete_inquiry(inquiry_id)

    return {"message": "문의글이 삭제되었습니다."}, 200


# 쿼리 파라미터로 검색, 정렬, 페이징된 문의글 목록을 조회
def get_filtered_inquiries(query):
    """
    쿼리 파라미터(keyword, page, size, sort)에 따라 필터링된 문의글 목록 조회
    """
    keyword = query.get("keyword")
    page = int(query.get("page", 1))
    size = int(query.get("size", 10))
    sort = query.get("sort", "latest")

    return inquiry_model.search_inquiries(keyword, page, size, sort), 200

