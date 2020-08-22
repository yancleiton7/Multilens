from urllib.parse import urljoin, urlparse

from flask import flash, redirect, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from multilens.ext.db.models import User

login_manager = LoginManager()


def init_app(app):
    login_manager.init_app(app)
    login_manager.login_view = "site.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(id=user_id)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def validate_user(username: str, password: str):
    user = User.get(user=username)
    if user is None:
        response = {"sucess": False, "message": "Usuario não cadastrado!"}

    elif check_password_hash(user.password, password):
        response = {
            "sucess": True,
            "message": "Usuario logado com sucesso!",
            "user": user,
        }

    else:
        response = {"sucess": False, "message": "Senha invalida"}

    return response


@login_manager.unauthorized_handler
def unauthorized():
    flash("Você precisa estar logado para acessar esta página.")
    return redirect(url_for("site.login", next=request.url))
