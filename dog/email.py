from flask import current_app
from flask_mail import Mail, Message
from threading import Thread

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
