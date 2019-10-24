import os

from flask import Flask, render_template, request, flash, redirect, session, abort

from app.database.story import Story
from app.database.user import User
from app.session_management import login_user, logout_user, current_user, login_required, no_login_required

app = Flask(__name__)

app.secret_key = os.urandom(64)


# this makes session more permanent
@app.before_request
def before_request():
    session.permanent = True


# this basically makes it so we can use current_user in any template we render
@app.context_processor
def make_template_globals():
    return dict(current_user=current_user())

#displays a starting page that allows a user to login/register
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Welcome', logged=current_user())

#page for user to login
@app.route('/login', methods=['GET', 'POST'])
@no_login_required
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
            login_user(to_login)
            flash('Logged In as [%s]' % to_login.username, 'green')
            return redirect('home')

    return render_template('login.html', title='login')

#page for user to register for the site
@app.route('/signup', methods=['GET', 'POST'])
@no_login_required
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


# user home
@app.route('/home')
@login_required
def home():
    return render_template('home.html', title='Home')


# logout user
@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out!', 'green')
    return redirect('index')


# this should be modified to display stories in the database
@app.route('/stories')
@login_required
def stories():
    storyThreads = [Story(1), Story(2), Story(3)]
    return render_template('stories.html', title='Stories', threads=storyThreads)


# this will be modified to display a story given an id
@app.route("/stories/<id>")
@login_required
def show_story(id):
    story = Story(id)
    return render_template('storythread.html', to_render=story)

#displays a user profile
@app.route("/users/<username>")
@login_required
def profile(username):
    if User.get_by_username(username) is not None:
        return render_template('profile.html', to_render=User.get_by_username(username))
    else:
        abort(404)

#displays a form to create a new story
@app.route('/stories/create/new', methods=['GET', 'POST'])
@login_required
def new_story():
    if 'title' in request.form.keys() and 'content' in request.form.keys():

        # read the data from the form
        # we can use [] now since we know the key exists
        title = request.form['title']
        content = request.form['content']

        # make sure that the form data is valid
        valid = True

        inrange = lambda a, b, c: b <= a <= c

        if not inrange(len(title), 3, 50):
            flash('Title should be between 3 and 50 characters!', 'red')
            valid = False

        if not (len(content), 10, 2500):
            flash('Story should be between 10 and 2500 characters!', 'red')
            valid = False
        if not valid:
            flash('Please fix the above errors before submitting the form again!', 'red')
        else:
            newstory_id = Story.new_story(current_user(), title, content)
            flash('Story created successfully', 'green')
            print(newstory_id)
            # return redirect(f'/stories/{newstory_id}')

    return render_template('newstory.html', title='New Story')
