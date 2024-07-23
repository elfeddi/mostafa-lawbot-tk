from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)


    from app.routes.auth import auth_bp
    from app.routes.file import file_bp
    from app.routes.query import query_bp
    from app.routes.chat import chat_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(file_bp, url_prefix='/file')
    app.register_blueprint(query_bp, url_prefix='/query')
    app.register_blueprint(chat_bp, url_prefix='/chat')

    return app
