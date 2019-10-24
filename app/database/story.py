from app.database import execute_command
from app.database.user import User

class Story:

    # initialize story with id
    def __init__(self, id):
        data = execute_command('SELECT * FROM `story` WHERE `story`.id=%d' % int(id)).fetchall()
        assert (len(data) != 0)  # no making non existing users!

        self.id = id
        self.content = "content_here"
        self.time = data[0][1]
        self.title = data[0][2]
        self.author = User(data[0][3])  # user id - maybe change to user object later
        self.first_addition = "first_addition"  # will be changed to a story_addition object

    # returns a list of story_addition objects
    def get_additions(self):
        pass

    # static methods

    # creates a new story
    @staticmethod
    def new_story(user, title, stater_text):
        execute_command(
            'INSERT INTO `story` '
            '(title, created_by) '
            'VALUES ("%s", %d);' % (title, user.id))

        # TODO: find a better way to do this lol
        inserted_id = int(execute_command(
            'SELECT id FROM `story` '
            'ORDER BY id DESC LIMIT 1').fetchall()[0][0])

        return inserted_id
