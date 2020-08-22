from flask import Flask

from multilens.ext import admin, auth, cli, config, db, site


def create_app():
    app = Flask(__name__)

    config.init_app(app)
    db.init_app(app)
    cli.init_app(app)
    site.init_app(app)
    auth.init_app(app)
    admin.init_app(app)

    return app
