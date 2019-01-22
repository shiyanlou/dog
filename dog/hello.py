from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    ua = request.headers.get('User-Agent')
    return render_template('index.html', ua=ua)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
