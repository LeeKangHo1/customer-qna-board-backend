# app/utils/jwt_util.py

import jwt
import datetime
from flask import request, jsonify
from functools import wraps

# JWT 시크릿 키와 알고리즘
from app.config import SECRET_KEY
ALGORITHM = 'HS256'

# JWT 토큰 생성 함수
def create_token(payload):
    """
    JWT 토큰 생성 함수
    payload: dict (예: {"id": 1, "is_admin": 0})
    """
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# JWT 토큰 디코딩 함수
def decode_token(token):
    """
    JWT 토큰 복호화 및 검증
    """
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        return {'error': '토큰이 만료되었습니다.'}
    except jwt.InvalidTokenError:
        return {'error': '유효하지 않은 토큰입니다.'}

# app/utils/jwt_util.py (계속)

# 일반 사용자 인증 데코레이터
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': '토큰이 필요합니다.'}), 401
        token = auth_header.split(' ')[1]
        decoded = decode_token(token)
        if 'error' in decoded:
            return jsonify({'message': decoded['error']}), 401
        request.user = decoded  # 인증된 사용자 정보를 request에 저장
        return f(*args, **kwargs)
    return decorated

# 관리자 인증 데코레이터
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': '토큰이 필요합니다.'}), 401
        token = auth_header.split(' ')[1]
        decoded = decode_token(token)
        if 'error' in decoded:
            return jsonify({'message': decoded['error']}), 401
        if not decoded.get('is_admin'):
            return jsonify({'message': '관리자 권한이 필요합니다.'}), 403
        request.user = decoded
        return f(*args, **kwargs)
    return decorated
