from flask import Blueprint, request, jsonify
from app.services.user_service import register_user, login_user

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
