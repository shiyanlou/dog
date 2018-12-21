from flask import Flask
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from .config import configs
from .models import db
from .handlers import front, mail

def register_blueprints(app):
    app.register_blueprint(front)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    bootstrap = Bootstrap(app)
    moment = Moment(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    register_blueprints(app)
    mail.init_app(app)
    
    return app
