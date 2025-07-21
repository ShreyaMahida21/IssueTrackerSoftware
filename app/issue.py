# app/issue.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from db import get_db

issue = Blueprint('issue', __name__)


@issue.route('/issues', methods=['GET', 'POST'])
@login_required
def track_issues():
    search_query = ''
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        search_query = request.form.get('search_query', '')
        query = f"SELECT * FROM issues WHERE title REGEXP ?"
        cur.execute("SELECT * FROM issues WHERE title LIKE ?", (f'%{search_query}%',))
    else:
        cur.execute("SELECT * FROM issues")

    issues = cur.fetchall()
    conn.close()

    return render_template('track_issues.html', issues=issues, search_query=search_query)


@issue.route('/issues/view/<int:issue_id>')
@login_required
def view_issue(issue_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM issues WHERE id = ?", (issue_id,))
    issue = cur.fetchone()
    conn.close()

    if not issue:
        flash("Issue not found.", "danger")
        return redirect(url_for('issue.track_issues'))

    return render_template('view_issue.html', issue=issue)


@issue.route('/issues/edit/<int:issue_id>', methods=['GET', 'POST'])
@login_required
def edit_issue(issue_id):
    # if current_user.role not in ['admin', 'superadmin']:
    #     flash("Unauthorized.", "danger")
    #     return redirect(url_for('issue.track_issues'))

    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        status = request.form['status']
        cur.execute("UPDATE issues SET status = ? WHERE id = ?", (status, issue_id))
        conn.commit()
        flash("Issue updated successfully.", "success")
        return redirect(url_for('issue.track_issues'))

    cur.execute("SELECT * FROM issues WHERE id = ?", (issue_id,))
    issue = cur.fetchone()
    conn.close()

    if not issue:
        flash("Issue not found.", "danger")
        return redirect(url_for('issue.track_issues'))

    return render_template('edit_issue.html', issue=issue)


@issue.route('/issues/delete/<int:issue_id>', methods=['GET'])
@login_required
def delete_issue(issue_id):
    # if current_user.role not in ['admin', 'superadmin']:
    #     flash("Unauthorized.", "danger")
    #     return redirect(url_for('issue.track_issues'))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
    conn.commit()
    conn.close()

    flash("Issue deleted.", "success")
    return redirect(url_for('issue.track_issues'))


@issue.route('/issues/create', methods=['GET', 'POST'])
@login_required
def create_issue():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        issue_type = request.form['type']
        status = 'Open'

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO issues (title, description, status, priority, type, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, status, priority, issue_type, current_user.username))
        conn.commit()
        conn.close()

        flash("Issue created successfully.", "success")
        return redirect(url_for('issue.track_issues'))

    return render_template('create_issue.html')
