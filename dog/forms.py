from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, \
    BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from .models import db, User
from .email import send_email


class RegisterForm(FlaskForm):
    name = StringField('名字', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(3, 12)])
    confirm_password = PasswordField('确认密码', validators=[DataRequired(), 
        EqualTo('password')])
    submit = SubmitField('提交')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('用户已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被存在')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        # 获得加密签名
        token = user.generate_confirm_token()
        send_email(self.email.data, user=user, token=token)


class LoginForm(FlaskForm):
    name = StringField('名字', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(3, 12)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_name(self, field):
        if not User.query.filter_by(name=field.data).first():
            raise ValidationError('用户不存在')

    def validate_password(self, field):
        user = User.query.filter_by(name=self.name.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码不正确')
