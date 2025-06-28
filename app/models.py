"""
models.py

Defines User class for Flask-Login.
"""

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.username = user_doc['username']
        self.role = user_doc['role']
