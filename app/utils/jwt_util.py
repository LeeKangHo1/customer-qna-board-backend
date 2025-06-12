import jwt
from datetime import datetime, timedelta
from app import config

def generate_token(payload, expires=1):
    payload["exp"] = datetime.utcnow() + timedelta(days=expires)
    return jwt.encode(payload, config.JWT_SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        return jwt.decode(token, config.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
