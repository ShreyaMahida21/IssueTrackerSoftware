"""
auth.py

Handles login, logout, register.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, logout_user
from . import mongo
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_doc = mongo.db.users.find_one({'username': username})
        if user_doc and user_doc['password'] == password:
            session.clear()
            session['username'] = username
            session['user_id'] = str(user_doc['_id'])
            login_user(User(user_doc))
            flash('✅ Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('❌ Invalid username or password.', 'danger')

    return render_template('login.html')

@auth.route('/logout')
def logout():
    """Logout page"""
    logout_user()
    session.clear()
    flash('✅ You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if mongo.db.users.find_one({'username': username}):
            flash('❌ Username already exists.', 'danger')
            return redirect(url_for('auth.register'))

        mongo.db.users.insert_one({
            'username': username,
            'password': password,
            'role': role
        })

        flash('✅ Registered successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')
