from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from db import db

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
