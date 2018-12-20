from flask import Blueprint

front = Blueprint('front', __name__)

@front.route('/', methods=['get', 'post'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(name=form.name.data)
            db.session.add(user)
            session['known'] = False
            send_email(form.name.data)
        else:
            session['known'] = True
        session['name'] = form.name.data
        flash('看起来你已经更名为：{}'.format(form.name.data), 'success')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known'))

@front.route('/user/<username>')
def user(username):
    ua = request.headers.get('User-Agent')
    return render_template('user.html', username=username, ua=ua,
        current_time=datetime.utcnow())
