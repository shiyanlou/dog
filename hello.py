from flask import Flask, request, render_template
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What\'s your name?', validators=[DataRequired()])
    submit = SubmitField('提交')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/用户/<username>')
def user(username):
    ua = request.headers.get('User-Agent')
    return render_template('user.html', username=username, ua=ua,
        current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def interval_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
