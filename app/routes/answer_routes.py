from flask import Blueprint

answer_bp = Blueprint("answer", __name__)

@answer_bp.route("/answers", methods=["GET"])
def get_answers():
    return {"message": "답변 목록입니다."}
