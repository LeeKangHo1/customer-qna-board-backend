from app.models import user_model
from app.utils.password_util import hash_password
import re

from app.models.user_model import find_by_login_id
from app.utils.password_util import check_password
from app.utils.jwt_util import create_token
from flask import abort

# 로그인
def login_user(data):
    login_id = data.get("login_id")
    password = data.get("password")

    user = find_by_login_id(login_id)
    if not user:
        abort(401, description="존재하지 않는 사용자입니다.")

    if not check_password(password, user["password"]):
        abort(401, description="비밀번호가 일치하지 않습니다.")

    token = create_token(user)  # user 딕셔너리 전체 전달

    return {
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "is_admin": bool(user["is_admin"])
        }
    }

# 회원 가입
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

def register_user(data):
    login_id = data.get("login_id")
    password = data.get("password")
    name = data.get("name")
    email = data.get("email")

    # 1. 필수값 확인
    if not login_id or not password or not name or not email:
        return {"error": "모든 항목을 입력하세요."}, 400

    # 2. 이메일 형식 확인
    if not re.match(EMAIL_REGEX, email):
        return {"error": "올바른 이메일 형식이 아닙니다."}, 400

    # 3. 중복 확인
    if user_model.find_by_login_id(login_id):
        return {"error": "이미 사용 중인 로그인 ID입니다."}, 409  # 충돌

    if user_model.find_by_email(email):
        return {"error": "이미 사용 중인 이메일입니다."}, 409

    # 4. 비밀번호 해시 및 저장
    hashed_pw = hash_password(password)
    user_model.insert_user(login_id, hashed_pw, name, email)

    # 5. 사용자 ID 다시 조회해서 리턴 (실무에서는 ID나 일부 데이터 반환)
    user = user_model.find_by_login_id(login_id)

    return {
        "id": user["id"],
        "login_id": user["login_id"],
        "name": user["name"]
    }, 201
