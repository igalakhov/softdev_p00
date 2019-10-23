from app.database import execute_command


class Story:

    # initialize story with id
    def __init__(self, id):
        data = execute_command('SELECT * FROM `story` WHERE `story`.id=%d' % id).fetchall()
        assert (len(data) != 0)  # no making non existing users!

        self.id = id
        self.content = "content_here"
        self.title = "title_here"
        self.time = "time_here"
        self.author = "author_here"  # will be changed to a user object
        self.first_addition = "id"  # will be changed to a story_addition object

    # returns a list of story_addition objects
    def get_additions(self):
        pass

    # static methods

    # creates a new story
    @staticmethod
    def new_story(user, stater_text):
        pass
