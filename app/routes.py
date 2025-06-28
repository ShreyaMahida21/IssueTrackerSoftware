"""
routes.py

Dashboard, issue management, and user management routes.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from datetime import datetime
from . import mongo

main = Blueprint('main', __name__)


# -------------------------------
# 🏠 DASHBOARD
# -------------------------------
@main.route('/')
@login_required
def home():
    """Dashboard showing counts"""
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


# -------------------------------
# 🟢 CREATE ISSUE
# -------------------------------
@main.route('/create_issue', methods=['GET', 'POST'])
@login_required
def create_issue():
    """Create a new issue"""
    if request.method == 'POST':
        issue = {
            "title": request.form['title'],
            "description": request.form['description'],
            "status": request.form['status'],
            "priority": request.form['priority'],
            "type": request.form['type'],
            "created_by": current_user.username,
            "assigned_to": request.form['assigned_to']
        }
        mongo.db.issues.insert_one(issue)
        flash('✅ Issue created successfully!', 'success')
        return redirect(url_for('main.create_issue'))

    # Get usernames for "Assigned To"
    users_cursor = mongo.db.users.find({}, {"username": 1})
    users = [user['username'] for user in users_cursor]

    return render_template('create_issue.html', users=users)


# -------------------------------
# 📋 TRACK ISSUES
# -------------------------------
@main.route('/track_issues')
@login_required
def track_issues():
    """Track all issues with pagination"""
    page = int(request.args.get('page', 1))
    per_page = 10
    skip = (page - 1) * per_page

    total_issues = mongo.db.issues.count_documents({})
    issues = list(mongo.db.issues.find().skip(skip).limit(per_page))

    has_next = total_issues > page * per_page
    has_prev = page > 1

    return render_template(
        'track_issues.html',
        issues=issues,
        page=page,
        has_next=has_next,
        has_prev=has_prev
    )


# -------------------------------
# 📝 UPDATE ISSUE
# -------------------------------
@main.route('/update_issue/<issue_id>', methods=['POST'])
@login_required
def update_issue(issue_id):
    """Update an issue and add to history"""
    issue = mongo.db.issues.find_one({'_id': ObjectId(issue_id)})
    old_status = issue['status']

    new_status = request.form['status']
    new_priority = request.form['priority']
    new_assigned_to = request.form['assigned_to']

    mongo.db.issues.update_one(
        {'_id': ObjectId(issue_id)},
        {'$set': {
            'status': new_status,
            'priority': new_priority,
            'assigned_to': new_assigned_to
        }}
    )

    change = {
        'issue_title': issue['title'],
        'changed_by': current_user.username,
        'change_description': f'Status changed from {old_status} to {new_status}',
        'timestamp': datetime.utcnow()
    }
    mongo.db.issue_history.insert_one(change)

    flash('✅ Issue updated successfully!', 'success')
    return redirect(url_for('main.track_issues'))


# -------------------------------
# ❌ DELETE ISSUE
# -------------------------------
@main.route('/delete_issue/<issue_id>', methods=['POST'])
@login_required
def delete_issue(issue_id):
    """Delete an issue"""
    mongo.db.issues.delete_one({'_id': ObjectId(issue_id)})
    flash('❌ Issue deleted!', 'success')
    return redirect(url_for('main.track_issues'))


# -------------------------------
# 📜 ISSUE HISTORY
# -------------------------------
@main.route('/issue_history/<issue_title>')
@login_required
def issue_history(issue_title):
    """View issue history"""
    history = list(mongo.db.issue_history.find({'issue_title': issue_title}))
    return render_template('issue_history.html', history=history, issue_title=issue_title)


# -------------------------------
# 👤 USER MANAGEMENT
# -------------------------------
@main.route('/users')
@login_required
def manage_users():
    """List all users"""
    users = list(mongo.db.users.find())
    return render_template('manage_users.html', users=users)


@main.route('/create_user', methods=['POST'])
@login_required
def create_user():
    """Create new user"""
    username = request.form['username']
    password = request.form['password']  # Plain text for now
    role = request.form['role']

    mongo.db.users.insert_one({
        'username': username,
        'password': password,
        'role': role
    })

    flash('✅ User created successfully!', 'success')
    return redirect(url_for('main.manage_users'))


@main.route('/update_user/<user_id>', methods=['POST'])
@login_required
def update_user(user_id):
    """Update user role and password"""
    role = request.form['role']
    new_password = request.form['new_password']

    update_fields = {'role': role}

    if new_password.strip():
        update_fields['password'] = new_password

    mongo.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': update_fields}
    )

    flash('✅ User updated successfully!', 'success')
    return redirect(url_for('main.manage_users'))


@main.route('/delete_user/<user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete a user"""
    mongo.db.users.delete_one({'_id': ObjectId(user_id)})
    flash('❌ User deleted!', 'success')
    return redirect(url_for('main.manage_users'))
