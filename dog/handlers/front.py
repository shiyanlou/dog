from datetime import datetime
from threading import Thread
from flask import Blueprint, session, redirect, url_for, render_template, flash, current_app
from flask_mail import Mail, Message
from ..forms import NameForm
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

@front.route('/', methods=['get', 'post'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(name=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            send_email(form.name.data)
        else:
            session['known'] = True
        session['name'] = form.name.data
        flash('看起来你已经更名为：{}'.format(form.name.data), 'success')
        return redirect(url_for('front.index'))
    return render_template(
        'index.html', 
        form=form, 
        name=session.get('name'), 
        known=session.get('known')
    )

@front.route('/user/<username>')
def user(username):
    ua = request.headers.get('User-Agent')
    return render_template('user.html', username=username, ua=ua,
        current_time=datetime.utcnow())

@front.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@front.errorhandler(500)
def interval_server_error(e):
    return render_template('500.html'), 500
