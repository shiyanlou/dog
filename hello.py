from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/用户/<username>')
def user(username):
    ua = request.headers.get('User-Agent')
    return render_template('user.html', username=username, ua=ua)

if __name__ == '__main__':
    app.run(debug=True)
