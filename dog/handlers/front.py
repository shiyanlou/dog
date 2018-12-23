from threading import Thread
from flask import Blueprint, session, redirect, url_for, render_template, flash, current_app
from flask_mail import Mail, Message
from flask_login import login_required, login_user, logout_user
from ..forms import RegisterForm, LoginForm
from ..models import db, User

front = Blueprint('front', __name__)
mail = Mail()

def send_async_email(msg):
    current_app.app_context().push()
    mail.send(msg)

def send_email(name, **kw):
    msg = Message(
        current_app.config.get('ADMIN'),
        sender=current_app.config.get('MAIL_USERNAME'),
        recipients=['yujiechi1a@163.com']
    )
    msg.html = '<h1>Hello, {} 加入</h1>'.format(name)
    mail.send(msg)
    '''
    thr = Thread(target=send_async_email, args=(msg,))
    thr.start()
    return thr
    '''

@front.route('/')
def index():
    return render_template('index.html')

@front.route('/register', methods=['get', 'post'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        session['name'] = form.name.data
        send_email(form.name.data)
        flash('{} 注册成功'.format(form.name.data), 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)

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
