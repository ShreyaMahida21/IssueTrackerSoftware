"""
Routes for Issue Tracker with SQLite.
Includes:
 - Dashboard
 - Create Issue
 - Track Issues (View, Edit, Delete)
 - Issue History (View Only)
 - Manage Users (Edit Password, Delete)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from db import get_db

main = Blueprint('main', __name__)

# ---------------- Dashboard ----------------
@main.route('/')
@login_required
def home():
    """ Dashboard showing stats """
    conn = get_db()
    cur = conn.cursor()
    total_users = cur.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    total_issues = cur.execute('SELECT COUNT(*) FROM issues').fetchone()[0]
    open_issues = cur.execute('SELECT COUNT(*) FROM issues WHERE status = ?', ('Open',)).fetchone()[0]
    closed_issues = cur.execute('SELECT COUNT(*) FROM issues WHERE status = ?', ('Resolved',)).fetchone()[0]
    conn.close()
    return render_template(
        'home.html',
        total_users=total_users,
        total_issues=total_issues,
        open_issues=open_issues,
        closed_issues=closed_issues
    )


# ---------------- Create Issue ----------------
@main.route('/create_issue', methods=['GET', 'POST'])
@login_required
def create_issue():
    """ Create new issue """
    conn = get_db()
    cur = conn.cursor()
    users = cur.execute('SELECT username FROM users').fetchall()
    user_list = [u[0] for u in users]

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        issue_type = request.form['type']
        assigned_to = request.form['assigned_to']

        try:
            cur.execute(
                'INSERT INTO issues (title, description, status, priority, type, created_by, assigned_to) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (title, description, 'Open', priority, issue_type, current_user.username, assigned_to)
            )
            conn.commit()
            flash('Issue created successfully!', 'success')
        except Exception as e:
            flash(f'Error creating issue: {e}', 'danger')
        finally:
            conn.close()
        return redirect(url_for('main.create_issue'))

    conn.close()
    return render_template('create_issue.html', users=user_list)


# ---------------- Track Issues ----------------
@main.route('/track_issues')
@login_required
def track_issues():
    """ List all issues (all statuses) """
    conn = get_db()
    cur = conn.cursor()
    issues = cur.execute('SELECT * FROM issues').fetchall()
    conn.close()
    return render_template('track_issues.html', issues=issues)


@main.route('/view_issue/<int:issue_id>')
@login_required
def view_issue(issue_id):
    """ View details for an issue """
    conn = get_db()
    cur = conn.cursor()
    issue = cur.execute('SELECT * FROM issues WHERE id = ?', (issue_id,)).fetchone()
    conn.close()
    return render_template('view_issue.html', issue=issue)


@main.route('/edit_issue/<int:issue_id>', methods=['GET', 'POST'])
@login_required
def edit_issue(issue_id):
    """ Edit an issue """
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        priority = request.form['priority']
        cur.execute(
            'UPDATE issues SET title=?, description=?, status=?, priority=? WHERE id=?',
            (title, description, status, priority, issue_id)
        )
        conn.commit()
        conn.close()
        flash('Issue updated!', 'success')
        return redirect(url_for('main.track_issues'))

    issue = cur.execute('SELECT * FROM issues WHERE id = ?', (issue_id,)).fetchone()
    conn.close()
    return render_template('edit_issue.html', issue=issue)


@main.route('/delete_issue/<int:issue_id>')
@login_required
def delete_issue(issue_id):
    """ Delete an issue """
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM issues WHERE id = ?', (issue_id,))
    conn.commit()
    conn.close()
    flash('Issue deleted!', 'info')
    return redirect(url_for('main.track_issues'))





# ---------------- Manage Users ----------------
@main.route('/manage_users')
@login_required
def manage_users():
    """ Show all users """
    conn = get_db()
    cur = conn.cursor()
    users = cur.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('manage_users.html', users=users)


@main.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """ Edit user password """
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        new_password = request.form['password']
        cur.execute('UPDATE users SET password = ? WHERE id = ?', (new_password, user_id))
        conn.commit()
        conn.close()
        flash('User password updated.', 'success')
        return redirect(url_for('main.manage_users'))

    user = cur.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return render_template('edit_user.html', user=user)


@main.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    """ Delete user """
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    flash('User deleted.', 'info')
    return redirect(url_for('main.manage_users'))
