"""
routes.py

Dashboard routes.
"""

from flask import Blueprint, render_template
from flask_login import login_required
from . import mongo

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def home():
    """Dashboard"""
    total_users = mongo.db.users.count_documents({})
    total_issues = mongo.db.issues.count_documents({})
    open_issues = mongo.db.issues.count_documents({'status': 'Open'})
    in_progress_issues = mongo.db.issues.count_documents({'status': 'In Progress'})
    resolved_issues = mongo.db.issues.count_documents({'status': 'Resolved'})

    return render_template(
        'home.html',
        total_users=total_users,
        total_issues=total_issues,
        open_issues=open_issues,
        in_progress_issues=in_progress_issues,
        resolved_issues=resolved_issues
    )
