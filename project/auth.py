import uuid

from flask import Blueprint, render_template, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db
from werkzeug.utils import redirect


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')
    remember = request.form.get('remember_me')
    name_in_base = User.query.filter_by(name=name).first()
    password_in_base = User.query.filter_by(password=password).first()
    if not name_in_base or not password_in_base:
        flash('Please check your name/password details and try again', 'warning')
        return redirect(url_for('auth.login'))
    if remember is not None:
        login_user(name_in_base, remember=True)
    else:
        login_user(name_in_base, remember=False)
    name_in_base.token = User.get_token(self=name_in_base)
    db.session.commit()
    return redirect(url_for('main.profile'))


@auth.route('/registration')
def registration():
    return render_template('registration.html')


@auth.route('/registration', methods=['POST'])
def registration_post():
    name = request.form.get('name')
    password = request.form.get('password')

    in_base = User.query.filter_by(name=name).first()
    if in_base:
        flash('This name is already in use.\n Please, enter another name', 'warning')
        return redirect(url_for('auth.registration'))

    new_user = User(public_id=str(uuid.uuid4()), name=name, password=password)
    db.session.add(new_user)
    db.session.commit()
    flash('Your registration was successful', 'success')
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
