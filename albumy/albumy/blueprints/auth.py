from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_user, current_user, logout_user, login_required, login_fresh, confirm_login

from albumy.extensions import db
from albumy.forms.auth import RegisterForm, LoginForm
from albumy.models import User
from albumy.utils import redirect_back


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        name = form.name.data
        email = form.email.data.lower()
        password = form.password.data
        user = User(name=name, username=username, email=email, confirmed=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Thanks for your register", "success")
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.validate_password(password):
            if login_user(user, remember_me):
                flash("Welcome back %s" % user.username, 'info')
                return redirect(url_for('user.index', username=username))
            else:
                flash('Your account is blocked', 'warning')
                return redirect(url_for('main.index'))

        flash("Wrong username or password", 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout", "info")
    return redirect(url_for('.login'))


@auth_bp.route('/re-authenticate', methods=['GET', 'POST'])
@login_required
def re_authenticate():
    if login_fresh():
        return redirect(url_for('user.index'))

    form = LoginForm()
    if form.validate_on_submit() and current_user.validate_password(form.password.data):
        confirm_login()
        return redirect_back()
    return render_template('auth/login.html', form=form)
