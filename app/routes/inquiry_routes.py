# ✅ inquiry_routes.py - 리팩터링

from flask import Blueprint, request, jsonify
from app.services import inquiry_service
from app.utils.jwt_util import token_required

inquiry_bp = Blueprint("inquiry", __name__)

# 문의글 등록 (POST /api/inquiries)
@inquiry_bp.route("/inquiries", methods=["POST"])
@token_required
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

# 필터링/전체 목록 조회 (GET /api/inquiries)
@inquiry_bp.route("/inquiries", methods=["GET"])
@token_required
def get_filtered_inquiries():
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
@token_required
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
@token_required
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
@token_required
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
