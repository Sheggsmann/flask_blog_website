from . import auth
from .. import db
from flask import render_template, redirect, url_for, request, flash, current_app
from .forms import LoginForm, RegisterForm
from ..models import User
from flask_login import login_user, logout_user, login_required, current_user
from ..utils import save_image


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('app.main.home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Login Successful', 'success')
            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith('/'):
                next_url = 'app.main.home'
            return redirect(url_for(next_url))
        flash('Invalid Credentials', 'warning')
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('app.main.home'))


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('app.main.home'))
    if form.validate_on_submit():
        if not 'picture' in request.files:
            filename = 'profile.png'
        else:
            filename = save_image(request.files['picture'])
        user = User(name=form.username.data, email=form.email.data, password=form.password.data,
         profile_picture=filename)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Login', 'success')
        return redirect(url_for('app.auth.login'))
    return render_template('register.html', form=form)

