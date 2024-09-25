from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    # Load environment variables
    flask_app = Flask(__name__)

    flask_app.config.from_object(Config)  # Config 클래스에서 설정 로드

    db.init_app(flask_app)

    # 다른 파일에서 정의된 라우트나 블루프린트 등록
    from .routes import main_routes
    flask_app.register_blueprint(main_routes)

    return flask_app
