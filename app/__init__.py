from flask import Flask
from flask_cors import CORS

# config와 블루프린트 import
from app import config
from app.routes.user_routes import user_bp
from app.routes.inquiry_routes import inquiry_bp
from app.routes.answer_routes import answer_bp

def create_app():
    app = Flask(__name__)

    # 환경 변수 등록
    app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY

    # CORS 허용 (모든 도메인)
    CORS(app)

    # Blueprint 등록 (라우터 등록)
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(inquiry_bp, url_prefix="/api")
    app.register_blueprint(answer_bp, url_prefix="/api")

    return app
