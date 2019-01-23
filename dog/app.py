from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from .models import db, User
from .config import configs

def register_blueprints(app):
    from .handler import front, user
    for i in [front, user]:
        app.register_blueprint(i)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    bootstrap = Bootstrap(app)
    moment = Moment(app)
    db.init_app(app)
    register_blueprints(app)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'), 500

    return app
