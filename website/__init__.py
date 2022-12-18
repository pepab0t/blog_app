from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pathlib import Path

db = SQLAlchemy()
DB_NAME: str = "database.db"

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "biggestsecret"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User, Post, Comment, Like

    create_database(app)

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = "auth.login" # type: ignore
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app: Flask):
    if not (Path("instance") / DB_NAME).exists():
        with app.app_context():
            db.create_all()
        print("Created database!")