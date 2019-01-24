from flask import render_template, Blueprint, request, session, redirect, url_for
from flask import flash
from datetime import datetime
from ..forms import NameForm
from ..models import db, User

front = Blueprint('front', __name__)

@front.route('/', methods=['get', 'post'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if not user:
            user = User(name=form.name.data, role_id=1)
            db.session.add(user)
            db.session.commit()
            flash('欢迎新用户：{}'.format(user.name), 'info')
            session['name'] = user.name
        else:
            flash('欢迎老用户，{}'.format(session.get("name")), 'info')
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'))
