from flask import Blueprint, request, jsonify
from app.services.user_service import register_user, login_user, delete_user_by_credential

user_bp = Blueprint("user", __name__)

# 로그인 (POST /api/login)
@user_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        response = login_user(data)
        return jsonify({
            "success": True,
            "response": response,
            "status": 200,
            "errorMessage": None
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "response": None,
            "status": 401,
            "errorMessage": str(e)
        }), 401

# 회원가입 (POST /api/users)
@user_bp.route("/users", methods=["POST"])
def register():
    try:
        data = request.get_json()
        response, status = register_user(data)
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


# 비밀번호 확인 후 회원 탈퇴 (DELETE /api/users)
@user_bp.route("/users", methods=["DELETE"])
def delete_user():
    try:
        data = request.get_json()
        response, status = delete_user_by_credential(data)

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

from app.services.user_service import update_user_info

# 회원정보 수정 (PUT /api/users/<user_id>)
@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.get_json()
        response, status = update_user_info(user_id, data)

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
    

from app.services.user_service import get_user_by_id

# 마이페이지 조회 (GET /api/users/<user_id>)
@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        response, status = get_user_by_id(user_id)

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

