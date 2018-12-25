from flask import current_app, render_template
from flask_mail import Mail, Message
from threading import Thread

mail = Mail()

def send_async_email(app, msg):
    #app.app_context().push()
    with app.app_context():
        print('--------------------- ok')
        mail.send(msg)

def send_email(to, **kw):
    # 如果使用线程，就不能用 current_app 了，它是一个代理，不是真正的应用对象
    # current_app 的上下文环境只支持传递给当前应用的主线程
    # 而 _get_current_object 方法可以返回一个应用对象
    # 该对象具有与 current_app 一样的上下文环境
    app = current_app._get_current_object()
    # Message 是个类，它接收以下参数：
    # 1、默认参数 subject 字符串（邮件主题
    # 2、sender 字符串（发件人的邮箱
    # 3、recipients 列表（收件人邮箱列表
    #print(app.config.get('MAIL_SUBJECT_PREFIX') + ' To ' + kw['user'].name)
    msg = Message(
        app.config.get('MAIL_SUBJECT_PREFIX') + ' To ' + kw['user'].name,
        sender=app.config.get('MAIL_USERNAME'),
        recipients=[to]
    )

    msg.body = render_template('email/confirm.txt', **kw)
    msg.html = render_template('email/confirm.html', **kw)
    '''
    mail.send(msg)
    '''
    # 创建一个子线程并启动
    thr = Thread(target=send_async_email, args=(app, msg))
    thr.start()
    return thr
