from datetime import datetime
from flask import Blueprint, render_template, request
from flask_login import login_required, login_user, logout_user

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/')
@login_required
def index():
    ua = request.headers.get('User-Agent')
    return render_template('user/user.html', ua=ua)
