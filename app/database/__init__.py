import sqlite3

db_file = 'database.db'


# establish db cursor connection here
def execute_command(cmd):
    db = sqlite3.connect('database.db')
    c = db.cursor()
    ret = c.execute(cmd)
    db.commit()
    return ret

# build the schema
# WARNING this will delete all the data in the database
def build_schema():
    # drop tables if the exist
    execute_command('DROP TABLE IF EXISTS `user`')
    execute_command('DROP TABLE IF EXISTS `story`')
    execute_command('DROP TABLE IF EXISTS `story_addition`')

    # create tables
    execute_command('CREATE TABLE `user` '
                    '(id INTEGER PRIMARY KEY, '
                    'username VARCHAR, '
                    'password BLOB, '
                    'time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')

    execute_command('CREATE TABLE `story`'
                    '(id INTEGER PRIMARY KEY,'
                    'time_created TIMESTAMP,'
                    'title VARCHAR,'
                    'created_by INTEGER)')

    execute_command('CREATE TABLE `story_addition`'
                    '(id INTEGER PRIMARY KEY,'
                    'time_created TIMESTAMP,'
                    'content VARCHAR,'
                    'story_id INTEGER,'
                    'author_id INTEGER)')
