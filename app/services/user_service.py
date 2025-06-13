import re
from flask import abort
from app.models import user_model
from app.utils.password_util import hash_password, check_password

# 로그인
def login_user(data):
    login_id = data.get("login_id")
    password = data.get("password")

    if not login_id or not password:
        abort(400, description="로그인 ID와 비밀번호를 입력하세요.")

    user = user_model.find_by_login_id(login_id)
    if not user:
        abort(401, description="존재하지 않는 사용자입니다.")

    if not check_password(password, user["password"]):
        abort(401, description="비밀번호가 일치하지 않습니다.")

    # JWT 제거됨 → 단순 성공 응답만 리턴
    return {
        "id": user["id"],
        "name": user["name"],
        "login_id": user["login_id"],
        "is_admin": bool(user["is_admin"])
    }

# 회원가입
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

def register_user(data):
    login_id = data.get("login_id")
    password = data.get("password")
    name = data.get("name")
    email = data.get("email")

    if not login_id or not password or not name or not email:
        return {"error": "모든 항목을 입력하세요."}, 400

    if not re.match(EMAIL_REGEX, email):
        return {"error": "올바른 이메일 형식이 아닙니다."}, 400

    if user_model.find_by_login_id(login_id):
        return {"error": "이미 사용 중인 로그인 ID입니다."}, 409

    if user_model.find_by_email(email):
        return {"error": "이미 사용 중인 이메일입니다."}, 409

    hashed_pw = hash_password(password)
    user_model.insert_user(login_id, hashed_pw, name, email)

    user = user_model.find_by_login_id(login_id)

    return {
        "id": user["id"],
        "login_id": user["login_id"],
        "name": user["name"]
    }, 201
