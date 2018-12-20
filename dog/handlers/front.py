from datetime import datetime
from threading import Thread
from flask import Blueprint, session, redirect, url_for

front = Blueprint('front', __name__)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(name, **kw):
    msg = Message(
        app.config.get('ADMIN'),
        sender=app.config.get('MAIL_USERNAME'),
        recipients=['yujiechi1a@163.com']
    )
    msg.html = '<h1>Hello, {} 加入</h1>'.format(name)
    thr = Thread(target=send_async_email, args=(app, msg))
    thr.start()
    return thr

@front.route('/', methods=['get', 'post'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(name=form.name.data)
            db.session.add(user)
            session['known'] = False
            send_email(form.name.data)
        else:
            session['known'] = True
        session['name'] = form.name.data
        flash('看起来你已经更名为：{}'.format(form.name.data), 'success')
        return redirect(url_for('index'))
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
