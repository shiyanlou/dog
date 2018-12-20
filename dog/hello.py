from threading import Thread
from flask import Flask, request, session, redirect, url_for, flash
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from .config import config

def create_app(config):
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    moment = Moment(app)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    mail = Mail(app)
    
    return app

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def interval_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
