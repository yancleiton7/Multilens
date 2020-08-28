from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user

from multilens.ext.auth import is_safe_url, validate_user

from .form import FormDoctor, FormLogin

bp = Blueprint("site", __name__)


@bp.route("/", methods=["GET"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("site.login"))

    return render_template("site/index.html")


@bp.route("/clientes", methods=["GET", "POST"])
@login_required
def clients():
    if request.method == "GET":
        return render_template("forms/clients.html", form=FormDoctor(request.form))

    elif request.method == "POST":
        flash("Doutor cadastrado com sucesso!", "is-success")
        return render_template("forms/clients.html", form=FormDoctor(request.form))


@bp.route("/cliente/<int:register>", methods=["GET"])
def client(register):
    return render_template("site/clients.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html", form=FormLogin(request.form))

    elif request.method == "POST":
        form = FormLogin(request.form)
        response = validate_user(form.username.data, form.passwd.data)

        next_url = request.args.get("next")
        if not is_safe_url(next_url):
            abort(400)

        if response["sucess"]:
            login_user(response["user"])

        else:
            flash(response["message"], "is-danger")

        return redirect(next_url or url_for("site.index"))


@bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("site.login"))


@bp.route("/venda/<int:order_id>", methods=["GET", "POST"])
def order(order_id):
    return render_template("auth/order.html")


@bp.route("/estoque", methods=["GET"])
def storage():
    return render_template("site/storage.html")


@bp.route("/vendas", methods=["GET"])
def sales():
    return render_template("site/sales.html")


@bp.route("/cadastrar_venda", methods=["GET", "POST"])
def register_sale():
    return render_template("site/products.html")
