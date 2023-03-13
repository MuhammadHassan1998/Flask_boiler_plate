from flaskr import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand


manager = Manager(create_app)

manager.add_command('db', MigrateCommand)

@manager.command
def runserver():
    manager.app.run()

if __name__ == "__main__":
    manager.run()


