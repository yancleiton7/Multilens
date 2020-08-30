from flask_migrate import Migrate, MigrateCommand, Manager
from multilens.ext.db import db

migrate = Migrate()

def init_app(app):
    migrate.init_app(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
