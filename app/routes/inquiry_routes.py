from flask import Blueprint

inquiry_bp = Blueprint("inquiry", __name__)

@inquiry_bp.route("/inquiries", methods=["GET"])
def get_inquiries():
    return {"message": "문의 목록입니다."}
