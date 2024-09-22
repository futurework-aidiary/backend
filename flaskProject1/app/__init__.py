from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()
app = Flask(__name__)

def create_app():
    # Load environment variables

    app.config.from_object(Config)  # Config 클래스에서 설정 로드

    db.init_app(app)

    # 다른 파일에서 정의된 라우트나 블루프린트 등록
    from .routes import main_routes
    app.register_blueprint(main_routes)

    with app.app_context():
        from . import routes  # Import routes to register them with the app

    return app
