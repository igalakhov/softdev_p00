# user class for interacting with the database
# using a class for database interaction instead of raw SQL makes code a lot more readable and simpler
# from bcrypt import hashpw, gensalt, checkpw

from app.database import execute_command
from . import story
import datetime

class User:

    def __init__(self, id):
        data = execute_command('SELECT * FROM `user` WHERE `user`.id=%d' % id).fetchall()
        assert (len(data) != 0)  # no making non existing users!
        self.id = int(data[0][0])
        self.username = data[0][1]
        self.password = data[0][2]
        self.time_created = data[0][3]

    def validate_password(self, to_validate):
        # TODO: probably make this secure?
        return self.password == to_validate

    def get_stories(self):
        data = execute_command('SELECT * FROM `story` WHERE `story`.created_by=%d' % self.id).fetchall()
        if len(data) == 0:
            return None
        stories = list()
        for s in data:
            stories.append(story.Story(s[0]))
        return stories

    def get_story_edits(self):
        data = execute_command('SELECT story_id FROM `story_addition` WHERE `story_addition`.author_id=%d' % self.id).fetchall()
        if len(data) == 0:
            return None
        stories = list()
        for s in data:
            stories.append(story.Story(s[0]))
        return stories

    # static methods

    # get user object by username
    @staticmethod
    def get_by_username(username):
        data = execute_command('SELECT id from `user` WHERE `user`.username = \"%s\"' % username).fetchall()
        if len(data) == 0:
            return None
        else:
            return User(data[0][0])

    # checks if username is avaliable
    @staticmethod
    def username_avaliable(username):
        res = execute_command('SELECT id FROM `user` WHERE `user`.username = \"%s\"' % username).fetchall()
        return len(res) == 0

    # creates a new user
    @staticmethod
    def new_user(username, password):

        execute_command('INSERT INTO `user` (username, password, time_created)'
                        'VALUES (\"%s\", \"%s\", \"%s\")' % (username, password, datetime.datetime.now()))
