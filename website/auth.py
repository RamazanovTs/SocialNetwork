from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('User does not exist', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()

        if user:
            flash("User already exists", category='error')
        elif password1 != password2:
            flash('Passwords must be equal', category='error')
        elif len(password1) < 6:
            flash('Passwords must be greater than 6 characters', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(password1,method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category="success")
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)
