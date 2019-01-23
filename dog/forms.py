from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name = StringField('名字', validators=[DataRequired()])
    submit = SubmitField('提交')
