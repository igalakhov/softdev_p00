from app.database import execute_command
from app.database.user import User
import datetime


class StoryAddition:

    # initialize addition with id
    def __init__(self, id):
        data = execute_command('SELECT * FROM `story_addition` WHERE `story_addition`.id=%d' % int(id)).fetchall()
        assert (len(data) != 0)  # no making non existing users!

        self.id = data[0][0]
        self.time_created = data[0][1]
        self.content = data[0][2]
        self.story_id = data[0][3]
        self.author = User(data[0][4])

    # static methods

    # creates a new story addition
    @staticmethod
    def new_story_addition(user, story, content):
        content = content.replace('"',r'""')
        execute_command('INSERT INTO `story_addition` (content, story_id, author_id, time_created)'
                        'VALUES (\"%s\", \"%s\", \"%s\", \"%s\")' % (content, story.id, user.id, datetime.datetime.now()))
