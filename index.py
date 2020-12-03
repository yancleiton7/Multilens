#Arquivo criado para o Vercel

from flask import Flask

from doceriah.ext import config


def create_app():
    app = Flask(__name__)
    config.init_app(app)

    return app

app = create_app()