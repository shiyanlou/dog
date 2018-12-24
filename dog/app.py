from flask import Flask, render_template
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import configs
from .models import db, User
from .handlers import front, user
from .email import mail

def register_blueprints(app):
    app.register_blueprint(front)
    app.register_blueprint(user)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    bootstrap = Bootstrap(app)
    moment = Moment(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    register_blueprints(app)
    mail.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'front.login'

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def interval_server_error(e):
        return render_template('500.html'), 500
    
    return app
