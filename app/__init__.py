import os

from flask import Flask, render_template, request, flash, redirect, session, abort

from app.database.story import Story
from app.database.story_addition import StoryAddition
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
            flash('That username does not belong to a registered account!','red')
            auth_valid = False
        elif not to_login.validate_password(password):
            flash('Incorrect password!','red')
            auth_valid = False

        if not valid or not auth_valid:
            flash('Please fix the above error(s) before submitting the form again!', 'red')
        else:
            # log in user
            login_user(to_login)
            flash('Logged In as [%s]' % to_login.username, 'green')
            return redirect('profile')

    return render_template('login.html', title='Log In')

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
            flash('Please fix the above error(s) before submitting the form again!', 'red')
        else:
            User.new_user(username, password)
            flash('Account created! Log In below!', 'green')
            return redirect('login')

        print(username, password, password_repeat)

    return render_template('signup.html', title='Sign Up')

#searches for story by title
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    storyThreads = []
    query = None
    if 'query' in request.form.keys() and len(request.form['query']) > 0:

        # read the data from the form
        # we can use [] now since we know the key exists

        #adds story to storyThreads if the search query is contained in the title
        query = request.form['query']
        for s in Story.get_all_stories():
            if query.lower() in s.title.lower():
                storyThreads.append(s)
    else:
        flash('Missing search query', 'red')
    return render_template('search.html', title='Search', threads=storyThreads, search=query)


# user profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='My Profile')

# other user profiles
@app.route('/profile/<username>')
@login_required
def userprofile(username):
    if username == current_user().username:
        return redirect("/profile")
    return render_template('userprofile.html', title=f"{username}'s Profile", to_render=User.get_by_username(username))


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
    storyThreads = Story.get_all_stories()
    return render_template('stories.html', title='Story Hub', threads=storyThreads)


# this will be modified to display a story given an id
@app.route("/stories/<id>", methods=['GET', 'POST'])
@login_required
def show_story(id):
    story = Story(id)
    has_added_to = current_user().id in story.added

    if 'addition' in request.form.keys():
        addition = request.form['addition']

        # make sure that the form data is valid
        valid = True

        inrange = lambda a, b, c: b <= a <= c

        if not inrange(len(addition), 10, 2500):
            flash('Story addition should be between 10 and 2500 characters!', 'red')
            valid = False
        if not valid:
            flash('Please fix the above error(s) before submitting the form again!', 'red')
        else:
            StoryAddition.new_story_addition(current_user(), story, addition)
            flash('Added successfully', 'green')
            return redirect(f'/stories/{id}')

    show = "show" in request.form.keys()

    return render_template('storythread.html', to_render=story, has_added_to = has_added_to, show_authors=show)

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

        if not inrange(len(content), 10, 2500):
            flash('Story should be between 10 and 2500 characters!', 'red')
            valid = False
        if not valid:
            flash('Please fix the above error(s) before submitting the form again!', 'red')
        else:
            newstory_id = Story.new_story(current_user(), title, content)
            s = Story(newstory_id)

            flash('Story created successfully', 'green')
            #print(newstory_id)
            return redirect(f'/stories/{newstory_id}')

    return render_template('newstory.html', title='New Story')
