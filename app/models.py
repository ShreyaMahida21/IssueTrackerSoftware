"""
Minimal user class with inheritance for Flask-Login.
"""

from flask_login import UserMixin

class BaseModel:
    """Base model to show basic inheritance."""
    def __init__(self):
        pass

class User(UserMixin, BaseModel):
    """
    User model for Flask-Login.
    Demonstrates simple inheritance.
    """
    def __init__(self, id, username, password, role):
        super().__init__()
        self.id = id
        self.username = username
        self.password = password
        self.role = role
