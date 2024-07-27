from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config

db = SQLAlchemy()

login = LoginManager()

login.login_view = 'routes.login'


def create_app(config_class=config.config["development"]):
    app = Flask(__name__)
    # Загрузка конфигурации
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)

    # импорт блупринтов
    from app.routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
