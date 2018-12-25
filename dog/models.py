from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    _password = db.Column('password', db.String(64), 
        nullable=False, default='dog')
    confirmed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
        onupdate=datetime.utcnow)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, p):
        self._password = generate_password_hash(p)

    def check_password(self, p):
        return check_password_hash(self._password, p)

    def generate_confirm_token(self, expiration=3600):
        # 创建一个令牌生成器，它可以用来生成令牌（就是一串复杂的字符串）
        # expiration 参数设置令牌的有效时间
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        # 令牌生成器的 dumps 方法的参数是字典，返回值就是令牌（也叫加密签名）
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        # 创建一个令牌生成器
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            # 令牌生成器的 loads 方法的参数是令牌，返回值为字典
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User: {}>'.format(self.name)

if __name__ == '__main__':
    db.create_all()
