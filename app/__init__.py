from flask import Flask, render_template, request

app = Flask(__name__)


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

        print(username, password, password_repeat)

    return render_template('signup.html', title='signup')
