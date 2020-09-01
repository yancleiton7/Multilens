from flask_migrate import Manager, Migrate, MigrateCommand

from multilens.ext.db import db

migrate = Migrate()


def init_app(app):
    migrate.init_app(app, db)
    manager = Manager(app)
    manager.add_command("db", MigrateCommand)
