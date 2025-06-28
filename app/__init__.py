"""
__init__.py

App factory setup: MongoDB, Flask-Login, Blueprints, User loader.
"""

from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from bson.objectid import ObjectId

mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')  # Make sure you have config.py with SECRET_KEY and MONGO_URI

    # Initialize MongoDB
    mongo.init_app(app)

    # Initialize Flask-Login
    login_manager.init_app(app)

    # Import User model here to avoid circular import
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        user_doc = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user_doc:
            return User(user_doc)
        return None

    # Register Blueprints
    from .auth import auth as auth_blueprint
    from .routes import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app
