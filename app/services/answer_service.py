from app.models import answer_model, inquiry_model, user_model

# 답변 등록
def create_answer(data):
    inquiry_id = data.get("inquiry_id")
    admin_id = data.get("admin_id")
    content = data.get("content")

    if not inquiry_id or not admin_id or not content:
        return {"error": "inquiry_id, admin_id, content는 필수입니다."}, 400

    inquiry = inquiry_model.find_inquiry_by_id(inquiry_id)
    if not inquiry:
        return {"error": "존재하지 않는 문의글입니다."}, 404

    admin = user_model.find_by_id(admin_id)
    if not admin or not admin["is_admin"]:
        return {"error": "관리자 권한이 필요합니다."}, 403

    answer_model.insert_answer(inquiry_id, admin_id, content)
    inquiry_model.update_status(inquiry_id, 'answered')  # 문의 상태 변경

    return {"message": "답변이 등록되었습니다."}, 201

# 답변 단일 조회
def get_answer_by_id(answer_id):
    answer = answer_model.find_answer_by_id(answer_id)
    if not answer:
        return {"error": "존재하지 않는 답변입니다."}, 404
    return answer, 200

# 문의글에 연결된 모든 답변 조회
def get_answers_by_inquiry(inquiry_id):
    return answer_model.find_answers_by_inquiry(inquiry_id), 200

# 답변 수정
def update_answer(answer_id, data):
    content = data.get("content")
    if not content:
        return {"error": "수정할 내용이 없습니다."}, 400

    answer = answer_model.find_answer_by_id(answer_id)
    if not answer:
        return {"error": "존재하지 않는 답변입니다."}, 404

    answer_model.update_answer(answer_id, content)
    return {"message": "답변이 수정되었습니다."}, 200

# 답변 삭제
def delete_answer(answer_id):
    answer = answer_model.find_answer_by_id(answer_id)
    if not answer:
        return {"error": "존재하지 않는 답변입니다."}, 404

    answer_model.delete_answer(answer_id)
    return {"message": "답변이 삭제되었습니다."}, 200
