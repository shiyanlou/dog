from flask import render_template, Blueprint, request, session, redirect, url_for
from flask import flash
from datetime import datetime
from ..forms import NameForm

front = Blueprint('front', __name__)

@front.route('/', methods=['get', 'post'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('看来你改了名字', 'info')
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'))
