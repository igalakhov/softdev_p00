import os

from flask import Flask, render_template, request, flash, redirect

from app.database.user import User
from app.database.story import Story

app = Flask(__name__)

app.secret_key = os.urandom(64)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='welcome')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # check if form was submitted
    if 'username' in request.form.keys() and \
            'password' in request.form.keys():
        # read the data from the form
        # we can use [] now since we know the key exists
        username = request.form['username']
        password = request.form['password']

        # make sure that the form data is valid
        valid = True

        inrange = lambda a, b, c: b <= a <= c

        if not inrange(len(username), 3, 12):
            flash('Username should be between 3 and 12 characters!', 'red')
            valid = False

        if not inrange(len(password), 3, 12):
            flash('Password should be between 3 and 12 characters!', 'red')
            valid = False

        to_login = User.get_by_username(username)

        auth_valid = True

        if to_login is None:
            auth_valid = False
        elif not to_login.validate_password(password):
            auth_valid = False

        if not valid or not auth_valid:
            flash('Please fix the above errors before submitting the form again!', 'red')
        else:
            # log in user
            flash('Logged In as [%s]' % to_login.username, 'green')

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
            flash('Account created! Log In below!', 'green')
            return redirect('login')

        print(username, password, password_repeat)

    return render_template('signup.html', title='signup')

#this should be modified to display stories in the database
@app.route('/stories')
def stories():
    storyThreads=[Story(1), Story(2), Story(3)]
    return render_template('stories.html', title='Stories', threads=storyThreads)

#this will be modified to display a story given an id
@app.route("/stories/<id>")
def show_story(id):
    story = Story(id)
    return render_template('storythread.html', title=story.title, thread=story)



@app.route('/stories/create/new')
def new_story():
    return "new story uwu"
