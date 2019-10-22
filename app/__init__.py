import os

from flask import Flask, render_template, request, flash
from app.database.user import User

app = Flask(__name__)

app.secret_key = os.urandom(64)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='welcome')


@app.route('/login')
def login():
    return render_template('login.html', title='login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # check if form was submitted
    if 'username' in request.form.keys() and \
            'password' in request.form.keys() and \
            'password_repeat' in request.form.keys():

        # read the data from the form
        # we can use [] now since we know the key exists
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password_repeat']

        # make sure that the form data is valid
        valid = True

        inrange = lambda a, b, c: b <= a <= c

        if not inrange(len(username), 3, 12):
            flash('Username should be between 3 and 12 characters!', 'red')
            valid = False

        if not inrange(len(password), 3, 12) or not inrange(len(password_repeat), 3, 12):
            flash('Password should be between 3 and 12 characters!', 'red')
            valid = False

        if not password == password_repeat:
            flash('Passwords do not match!', 'red')
            valid = False

        if not User.username_avaliable(username):
            flash('Username already taken!', 'red')
            valid = False

        if not valid:
            flash('Please fix the above errors before submitting the form again!', 'red')
        else:
            User.new_user(username, password)
            flash('Account created!', 'green')

        print(username, password, password_repeat)

    return render_template('signup.html', title='signup')

@app.route('/stories')
def stories():
    return render_template('stories.html', title='Stories')

@app.route('/stories/create/new')
def newStory():
    return "new story uwu"
