class Story:

    # initialize story with id
    def __init__(self,id):
        self.id = id
        self.content = "content_here"
        self.title = "title_here"
        self.author = "author_here" #will be changed to a user object
        self.time = "time_here"
        self.first_addition = "id" #will be changed to a story_addition object

    # returns a list of story_addition object
    def get_additions(self):
        pass
