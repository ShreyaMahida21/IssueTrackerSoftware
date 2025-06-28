# app/issue.py
from flask import Blueprint

issue = Blueprint('issue', __name__)

@issue.route('/issue')
def issue_home():
    return "Issue management coming soon."
