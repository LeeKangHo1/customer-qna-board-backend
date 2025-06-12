import jwt
from datetime import datetime, timedelta
from app import config

# 토큰 생성
def generate_token(payload, expires_days=1):
    payload["exp"] = datetime.utcnow() + timedelta(days=expires_days)
    return jwt.encode(payload, config.JWT_SECRET_KEY, algorithm="HS256")

# 토큰 검증
def decode_token(token):
    try:
        return jwt.decode(token, config.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None  # 토큰 만료
    except jwt.InvalidTokenError:
        return None  # 잘못된 토큰
