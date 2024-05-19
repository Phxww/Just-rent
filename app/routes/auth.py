from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User
from enum import Enum, unique

auth = Blueprint('auth', __name__)


@unique
class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.view_cars'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            flash('Email and password are required!')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            if current_user.role.value == UserRole.ADMIN.value:
                return redirect(url_for('admin.admin_cars'))
            else:
                return redirect(url_for('main.view_cars'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if not all([username, email, password, confirm_password]):
            flash('All fields are required!')
            return redirect(url_for('auth.signup'))

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('auth.signup'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken')
            return redirect(url_for('auth.signup'))

        if User.query.filter_by(email=email).first():
            flash('Email already in use')
            return redirect(url_for('auth.signup'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please login.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')
