# ✅ answer_routes.py - 리팩터링

from flask import Blueprint, request, jsonify
from app.services import answer_service
from app.utils.jwt_util import token_required, admin_required

answer_bp = Blueprint("answer", __name__)

# 답변 등록 (POST /api/answers)
@answer_bp.route("/answers", methods=["POST"])
@admin_required
def create_answer():
    try:
        data = request.get_json()
        response, status = answer_service.create_answer(data)
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

# 단일 답변 조회 (GET /api/answers/<id>)
@answer_bp.route("/answers/<int:answer_id>", methods=["GET"])
@token_required
def get_answer(answer_id):
    try:
        response, status = answer_service.get_answer_by_id(answer_id)
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

# 특정 문의글의 답변 목록 조회 (GET /api/answers?inquiry_id=1)
@answer_bp.route("/answers", methods=["GET"])
@token_required
def get_answers_by_inquiry():
    try:
        inquiry_id = request.args.get("inquiry_id", type=int)
        if not inquiry_id:
            return jsonify({
                "success": False,
                "response": None,
                "status": 400,
                "errorMessage": "inquiry_id는 필수입니다."
            }), 400
        response, status = answer_service.get_answers_by_inquiry(inquiry_id)
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

# 답변 수정 (PUT /api/answers/<id>)
@answer_bp.route("/answers/<int:answer_id>", methods=["PUT"])
@admin_required
def update_answer(answer_id):
    try:
        data = request.get_json()
        response, status = answer_service.update_answer(answer_id, data)
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

# 답변 삭제 (DELETE /api/answers/<id>)
@answer_bp.route("/answers/<int:answer_id>", methods=["DELETE"])
@admin_required
def delete_answer(answer_id):
    try:
        response, status = answer_service.delete_answer(answer_id)
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
