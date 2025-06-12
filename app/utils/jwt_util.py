import jwt
import datetime
import os
from dotenv import load_dotenv
from flask import request, jsonify

# .env 로부터 환경 변수 불러오기
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET", "default_secret")
ALGORITHM = "HS256"

# ✅ JWT 토큰 생성 함수
def create_token(user):
    payload = {
        "id": user["id"],
        "name": user["name"],
        "is_admin": user["is_admin"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# ✅ JWT 토큰 디코드 및 검증 함수
def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # 토큰 만료
    except jwt.InvalidTokenError:
        return None  # 유효하지 않은 토큰

# ✅ 요청 헤더에서 토큰 추출 및 검증 (데코레이터로 사용 가능)
def get_user_from_request():
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        user = decode_token(token)
        return user
    return None
