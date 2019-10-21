from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='welcome')


@app.route('/login')
def login():
    return render_template('login.html', title='login')


@app.route('/signup')
def signup():
    return render_template('signup.html', title='signup')
