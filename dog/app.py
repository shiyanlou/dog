from flask import Flask
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
from flask_mail import Mail, Message
from .config import config
from .models import db

def register_blueprints(app):
    from .handlers import front
    app.register_blueprint(front)

def create_app(config):
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    moment = Moment(app)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    register_blueprints(app)
    mail = Mail(app)
    
    return app

class NameForm(FlaskForm):
    name = StringField('What\'s your name?', validators=[DataRequired()])
    submit = SubmitField('提交')
