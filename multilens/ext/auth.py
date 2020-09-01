from datetime import timedelta

from flask import flash, redirect, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from multilens.ext.db.models import User

login_manager = LoginManager()


def init_app(app):
    login_manager.init_app(app)
    login_manager.login_view = "site.login"
    app.permanent_session_lifetime = timedelta(hours=1)


@login_manager.user_loader
def load_user(user_id):
    return User.get(id=user_id)


def validate_user(username: str, password: str):
    user = User.get(user=username)
    if user is None:
        response = {"success": False, "message": "Usuario não cadastrado!"}

    elif check_password_hash(user.password, password):
        response = {
            "success": True,
            "message": "Usuario logado com successo!",
            "user": user,
        }

    else:
        response = {"success": False, "message": "Senha invalida"}

    return response


@login_manager.unauthorized_handler
def unauthorized():
    flash("Você precisa estar logado para acessar esta página.", "is-danger")
    return redirect(url_for("site.login", next=request.url))
