from datetime import timedelta

from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from doceriah.ext.db.models import User
from doceriah.ext.site import is_safe_url
from doceriah.ext.site.form import FormLogin

login_manager = LoginManager()


def init_app(app):
    login_manager.init_app(app)
    login_manager.login_view = "login"
    app.permanent_session_lifetime = timedelta(hours=1)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("auth/login.html", form=FormLogin(request.form))

        elif request.method == "POST":
            form = FormLogin(request.form)
            response = validate_user(form.username.data, form.passwd.data)

            next_url = request.args.get("next")
            if not is_safe_url(next_url):
                abort(400)

            if response["success"]:
                login_user(response["user"])

            else:
                flash(response["message"], "is-danger")

            return redirect(next_url or url_for("site.index"))

    @app.route("/logout", methods=["GET"])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))


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
    return redirect(url_for("login", next=request.url))
