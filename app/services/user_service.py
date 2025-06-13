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

# 로그인 ID와 비밀번호를 확인한 후 탈퇴 처리하는 함수
def delete_user_by_credential(data):
    login_id = data.get("login_id")
    password = data.get("password")

    if not login_id or not password:
        return {"error": "로그인 ID와 비밀번호를 입력하세요."}, 400

    user = user_model.find_by_login_id(login_id)
    if not user:
        return {"error": "존재하지 않는 사용자입니다."}, 404

    if not check_password(password, user["password"]):
        return {"error": "비밀번호가 일치하지 않습니다."}, 401

    user_model.delete_user(user["id"])

    return {"message": "회원 탈퇴가 완료되었습니다."}, 200

# 사용자 정보를 수정하는 함수 (이름, 이메일, 비밀번호 변경 가능)
def update_user_info(user_id, data):
    login_id = data.get("login_id")
    password = data.get("password")
    new_name = data.get("new_name")
    new_email = data.get("new_email")
    new_password = data.get("new_password")

    if not login_id or not password:
        return {"error": "로그인 ID와 비밀번호는 필수입니다."}, 400

    user = user_model.find_by_id(user_id)
    if not user:
        return {"error": "존재하지 않는 사용자입니다."}, 404

    if user["login_id"] != login_id:
        return {"error": "ID가 일치하지 않습니다."}, 403

    if not check_password(password, user["password"]):
        return {"error": "비밀번호가 일치하지 않습니다."}, 401

    # 이메일 중복 확인 (현재 이메일 제외)
    if new_email and new_email != user["email"]:
        existing_user = user_model.find_by_email(new_email)
        if existing_user:
            return {"error": "이미 사용 중인 이메일입니다."}, 409

    # 새로운 비밀번호 해싱
    hashed_pw = hash_password(new_password) if new_password else None

    # DB 업데이트
    user_model.update_user(user_id, new_name, new_email, hashed_pw)

    return {"message": "회원정보가 수정되었습니다."}, 200

# 사용자 ID로 사용자 정보를 조회하는 함수
def get_user_by_id(user_id):
    user = user_model.find_by_id(user_id)

    if not user:
        return {"error": "존재하지 않는 사용자입니다."}, 404

    return {
        "id": user["id"],
        "login_id": user["login_id"],
        "name": user["name"],
        "email": user["email"],
        "is_admin": bool(user["is_admin"]),
        "created_at": user["created_at"]
    }, 200

