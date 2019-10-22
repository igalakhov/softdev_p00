# user class for interacting with the database
# using a class for database interaction instead of raw SQL makes code a lot more readable and simpler
from bcrypt import hashpw, gensalt

from app.database import execute_command


class User:

    def __init__(self, id):
        self.username = ''
        self.password = ''
        self.time_created = 00

    def validate_password(self, to_validate):
        pass

    def get_stories(self):
        pass

    def get_story_edits(self):
        pass

    # static methods

    # checks if username is avaliable
    @staticmethod
    def username_avaliable(username):
        res = execute_command('SELECT id FROM `user` WHERE `user`.username = \"%s\"' % username).fetchall()
        return res == []

    # creates a new user
    @staticmethod
    def new_user(username, password):
        hashed_pass = str(hashpw(password.encode(), gensalt(12))).replace('b', '').replace('\'', '')

        execute_command('INSERT INTO `user` (username, password)'
                        'VALUES (\"%s\", \"%s\")' % (username, hashed_pass))
