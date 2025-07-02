"""
Flask app factory with raw SQLite setup.
"""

from flask import Flask
from flask_login import LoginManager
from config import Config
from db import init_db

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    """
    Create and configure the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    from .routes import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    # Initialize DB
    init_db()

    return app
