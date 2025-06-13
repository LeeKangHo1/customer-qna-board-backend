from flask import Blueprint, request, jsonify
from app.services import inquiry_service

inquiry_bp = Blueprint("inquiry", __name__)

# 문의글 등록 (POST /api/inquiries)
@inquiry_bp.route("/inquiries", methods=["POST"])
def create_inquiry():
    try:
        data = request.get_json()
        response, status = inquiry_service.create_inquiry(data)
        return jsonify({
            "success": status == 201,
            "response": response if status == 201 else None,
            "status": status,
            "errorMessage": None if status == 201 else response.get("error")
        }), status
    except Exception as e:
        return jsonify({
            "success": False,
            "response": None,
            "status": 500,
            "errorMessage": str(e)
        }), 500


# 전체 목록 조회 (GET /api/inquiries) - 관리자 or 필터링
@inquiry_bp.route("/inquiries", methods=["GET"])
def get_all_inquiries():
    try:
        response, status = inquiry_service.get_all_inquiries()
        return jsonify({
            "success": True,
            "response": response,
            "status": status,
            "errorMessage": None
        }), status
    except Exception as e:
        return jsonify({
            "success": False,
            "response": None,
            "status": 500,
            "errorMessage": str(e)
        }), 500
    
# GET /api/inquiries?keyword=검색어&page=1&size=10&sort=latest
@inquiry_bp.route("/inquiries", methods=["GET"])
def get_filtered_inquiries():  # ✅ 함수 이름 변경
    try:
        query = request.args
        response, status = inquiry_service.get_filtered_inquiries(query)
        return jsonify({
            "success": True,
            "response": response,
            "status": status,
            "errorMessage": None
        }), status
    except Exception as e:
        return jsonify({
            "success": False,
            "response": None,
            "status": 500,
            "errorMessage": str(e)
        }), 500



# 단일 문의글 조회 (GET /api/inquiries/<id>)
@inquiry_bp.route("/inquiries/<int:inquiry_id>", methods=["GET"])
def get_inquiry(inquiry_id):
    try:
        response, status = inquiry_service.get_inquiry_by_id(inquiry_id)
        return jsonify({
            "success": status == 200,
            "response": response if status == 200 else None,
            "status": status,
            "errorMessage": None if status == 200 else response.get("error")
        }), status
    except Exception as e:
        return jsonify({
            "success": False,
            "response": None,
            "status": 500,
            "errorMessage": str(e)
        }), 500


# 문의글 수정 (PUT /api/inquiries/<id>)
@inquiry_bp.route("/inquiries/<int:inquiry_id>", methods=["PUT"])
def update_inquiry(inquiry_id):
    try:
        data = request.get_json()
        response, status = inquiry_service.update_inquiry(inquiry_id, data)
        return jsonify({
            "success": status == 200,
            "response": response if status == 200 else None,
            "status": status,
            "errorMessage": None if status == 200 else response.get("error")
        }), status
    except Exception as e:
        return jsonify({
            "success": False,
            "response": None,
            "status": 500,
            "errorMessage": str(e)
        }), 500


# 문의글 삭제 (DELETE /api/inquiries/<id>)
@inquiry_bp.route("/inquiries/<int:inquiry_id>", methods=["DELETE"])
def delete_inquiry(inquiry_id):
    try:
        response, status = inquiry_service.delete_inquiry(inquiry_id)
        return jsonify({
            "success": status == 200,
            "response": response if status == 200 else None,
            "status": status,
            "errorMessage": None if status == 200 else response.get("error")
        }), status
    except Exception as e:
        return jsonify({
            "success": False,
            "response": None,
            "status": 500,
            "errorMessage": str(e)
        }), 500

