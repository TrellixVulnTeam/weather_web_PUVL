from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Th1s1ss3cr3t'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/janki/Desktop/Python/weather_web/project/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    from .models import Item

    @login_manager.user_loader
    def load_user(public_id):
        return User.query.get(int(public_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from project.api.api_main import api_main as api_main_blueprint
    app.register_blueprint(api_main_blueprint)
    from project.api.api_auth import api_auth as api_auth_blueprint
    app.register_blueprint(api_auth_blueprint)

    return app
