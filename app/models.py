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
class Issue(BaseModel):
    """
    Issue model that represents a bug/feature/task in the tracker.
    """
    def __init__(self, id, title, description, status, priority, type, created_by, assigned_to):
        super().__init__()
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.type = type
        self.created_by = created_by
        self.assigned_to = assigned_to
