"""
__init__.py

App factory setup: MongoDB, Flask-Login, blueprints, user loader.
"""

from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from bson.objectid import ObjectId

# Create app
app = Flask(__name__)
app.config.from_object('config')

# Setup PyMongo
mongo = PyMongo(app)

# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Import User
from .models import User

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user_doc = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user_doc:
        return User(user_doc)
    return None

# Blueprints
from .auth import auth as auth_blueprint
from .routes import main as main_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)
