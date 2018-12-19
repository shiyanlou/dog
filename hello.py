import os
from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# 这两行给应用注册 Mail 
from flask_mail import Mail
mail = Mail(app)

basedir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
# SERVER 和 PORT 是需要网上查的，各家的邮箱都不同
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 25
# 下面这俩通常这么设置
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# USERNAME 是发信人的邮箱，PASSWORD 是从邮箱那里获得的授权码
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# 有了以上设置，可以在 flask shell 里执行下面的代码
# 结果就是 QQ 邮箱会给 163 邮箱发送一封邮件
'''
from flask_mail import Message
from hello import mail
msg = Message('test',                   # 邮件标题
    sender='1195581533@qq.com',         # 发件人
    recipients=['yujiechi1a@163.com']   # 收件人列表
)
msg.body = 'test body'                  # 邮件正文
msg.html = '<b>HTML</b> body'           # 这个也是，不知道哪个是，待测试
with app.app_context():                 # 这行可以不写，毕竟用了 flask shell
    mail.send(msg)
'''
app.config['SECRET_KEY'] = 'HELLO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    def __repr__(self):
        return '<User: {}>'.format(self.name)

class NameForm(FlaskForm):
    name = StringField('What\'s your name?', validators=[DataRequired()])
    submit = SubmitField('提交')

@app.route('/', methods=['get', 'post'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(name=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        flash('看起来你已经更名为：{}'.format(form.name.data), 'success')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known'))

@app.route('/user/<username>')
def user(username):
    ua = request.headers.get('User-Agent')
    return render_template('user.html', username=username, ua=ua,
        current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def interval_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
