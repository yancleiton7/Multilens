from werkzeug.security import check_password_hash

from multilens.ext.db import db
from multilens.ext.db.models import User


def create_db():
    """Cria o banco de dados"""
    db.create_all()


def drop_db():
    """Limpa o banco de dados"""
    db.drop_all()
