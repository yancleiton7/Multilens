#Arquivo criado para o Vercel

from flask import Flask

from multilens.ext import config


def create_app():
    app = Flask(__name__)
    config.init_app(app)

    return app
