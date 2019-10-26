from functools import wraps

from flask import session, redirect, flash, request

from app.database.user import User


# get current logged in user
def current_user():
    if 'user_id' in session:
        return User(session['user_id'])
    return None


# login a user
# usr is a User object
def login_user(usr):
    session['user_id'] = usr.id


# clear session (logout user)
def logout_user():
    session.clear()


# decorator for checking login
def login_required(f):
    @wraps(f)
    def dec(*args, **kwargs):
        if 'user_id' in session:
            for arg in args:
                print(arg)
            return f(*args, **kwargs)
        flash('You must be logged in to view [%s]!' % request.path, 'red')
        return redirect('/login')

    return dec


# decorator for checking no lgoin
def no_login_required(f):
    @wraps(f)
    def dec(*args, **kwargs):
        if 'user_id' not in session:
            return f(*args, **kwargs)
        flash('You cannot view [%s] while logged in!' % request.path, 'red')
        return redirect('/home')

    return dec
