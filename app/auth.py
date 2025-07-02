"""
Authentication routes using raw SQLite queries.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .models import User
from db import get_db
from . import login_manager

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    """
    Load user by ID for Flask-Login session.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return User(row['id'], row['username'], row['password'], row['role'])
    return None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cur.fetchone()
        conn.close()

        if row and row['password'] == password:
            user = User(row['id'], row['username'], row['password'], row['role'])
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                (username, password, role)
            )
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception:
            flash('Username already exists.', 'danger')
        finally:
            conn.close()

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    """
    Log the user out.
    """
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
