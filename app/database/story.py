from app.database import execute_command
from app.database.user import User
from app.database.story_addition import StoryAddition
import datetime

class Story:

    # initialize story with id
    def __init__(self, id):
        data = execute_command('SELECT * FROM `story` WHERE `story`.id=%d' % int(id)).fetchall()
        assert (len(data) != 0)
        added = execute_command('SELECT author_id FROM `story_addition` WHERE `story_addition`.story_id=%d' % int(id)).fetchall()
        self.id = id
        self.time_created = data[0][1]
        self.title = data[0][2]
        self.author = User(data[0][3])  # user id - maybe change to user object later
        self.added = list()  # ids of all the users who added to the story
        for a in added:
            self.added.append(a[0])

    # returns a list of story_addition objects
    def get_additions(self):
        story_addition = execute_command('SELECT * FROM `story_addition` ').fetchall()
        additions = execute_command(
            'SELECT id FROM `story_addition` WHERE story_id=%d' % int(self.id)).fetchall()
        a = list()
        for addition in additions:
            a.append(StoryAddition(addition[0]))
        return a

    # static methods

    # creates a new story
    @staticmethod
    def new_story(user, title, content):
        execute_command(
            'INSERT INTO `story` '
            '(title, created_by, time_created) '
            'VALUES ("%s", %d, "%s");' % (title, user.id, datetime.datetime.now()))

        # TODO: find a better way to do this lol
        inserted_id = int(execute_command(
            'SELECT id FROM `story` '
            'ORDER BY id DESC LIMIT 1').fetchall()[0][0])

        StoryAddition.new_story_addition(user, Story(inserted_id), content)
        return inserted_id

    @staticmethod
    def get_all_stories():
        data = execute_command(
            'SELECT id FROM `story` '
            'ORDER BY id DESC').fetchall()

        stories = list()
        for s in data:
            stories.append(Story(s[0]))
        return stories
