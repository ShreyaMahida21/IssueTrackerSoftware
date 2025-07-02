import os

class Config:
    """Application configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecret'
    DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'issuetracker.db')
