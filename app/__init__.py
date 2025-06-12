from flask import Flask
from flask_cors import CORS
from app.routes.user_routes import user_bp
from app.routes.inquiry_routes import inquiry_bp
from app.routes.answer_routes import answer_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    CORS(app)

    # 블루프린트 등록
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(inquiry_bp, url_prefix="/api")
    app.register_blueprint(answer_bp, url_prefix="/api")

    return app
