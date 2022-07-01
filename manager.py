from flask_script import Manager
from app import app_created, db
from flask_migrate import Migrate, MigrateCommand

app = app_created('develop')
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
