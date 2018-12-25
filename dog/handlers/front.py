from flask import Blueprint, session, redirect, url_for, render_template, \
    flash, current_app
from flask_login import login_required, login_user, logout_user, current_user
from ..forms import RegisterForm, LoginForm
from ..models import db, User

front = Blueprint('front', __name__)

@front.route('/')
def index():
    return render_template('index.html')

@front.route('/register', methods=['get', 'post'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        session['name'] = form.name.data
        flash('{} 注册成功'.format(form.name.data), 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)

@front.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('.index'))

@front.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        login_user(user)
        flash('您已成功登录', 'success')
        return redirect(url_for('.index'))
    return render_template('login.html', form=form, name=session.get('name'))

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录', 'info')
    return redirect(url_for('.index'))

@front.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@front.errorhandler(500)
def interval_server_error(e):
    return render_template('500.html'), 500
