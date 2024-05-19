from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import Config
from flask_wtf import CSRFProtect
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login = LoginManager()
login.login_view = 'auth.login'


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)


    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.routes.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from app.routes.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app
