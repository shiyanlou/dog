from flask import Blueprint, render_template

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('<name>')
def index(name):
    return render_template('user.html', name=name)
