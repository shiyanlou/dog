from flask import render_template
from .front import front

@front.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@front.errorhandler(500)
def interval_server_error(e):
    return render_template('500.html'), 500
