from urllib.parse import urljoin, urlparse

from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user

from multilens.ext.auth import validate_user
from multilens.ext.db.models import Doctor, Institution

from .form import FormDoctor, FormInstitution, FormLogin

bp = Blueprint("site", __name__)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


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


@bp.route("/", methods=["GET"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("site.login"))

    return render_template("site/index.html")


@bp.route("/medicos/", methods=["GET"])
@login_required
def doctors():
    return render_template("site/doctors.html", doctors=Doctor.get_all())


@bp.route("/medicos/cadastro", methods=["GET", "POST"])
@login_required
def form_doctor():
    form = FormDoctor()
    if request.method == "GET":
        return render_template("forms/doctors.html", form=form)

    elif request.method == "POST":
        if form.validate_on_submit():
            doctor = Doctor()
            form.populate_obj(doctor)
            doctor.save()
            flash("Doutor cadastrado com sucesso!", "is-success")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

        return render_template("forms/doctors.html", form=form)


@bp.route("/medicos/<int:register>", methods=["GET"])
@login_required
def doctor(register):
    return render_template("site/doctor.html")


@bp.route("/instituicoes/", methods=["GET"])
def institutions():
    return render_template("site/institution.html", institutions=Institution.get_all())


@bp.route("/instituicoes/cadastro", methods=["GET", "POST"])
@login_required
def form_institution():
    form = FormInstitution()
    if request.method == "GET":
        return render_template("forms/institution.html", form=form)

    elif request.method == "POST":
        if form.validate_on_submit():
            institution = Institution()
            form.populate_obj(institution)
            institution.save()
            flash("Instituição cadastrada com sucesso!", "is-success")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    return render_template("forms/institution.html", form=form)


@bp.route("/vendas/<int:order_id>", methods=["GET", "POST"])
@login_required
def order(order_id):
    return render_template("auth/order.html")


@bp.route("/estoque", methods=["GET"])
@login_required
def storage():
    return render_template("site/storage.html")


@bp.route("/vendas/", methods=["GET"])
@login_required
def sales():
    return render_template("site/sales.html")


@bp.route("/vendas/nova", methods=["GET", "POST"])
@login_required
def register_sale():
    return render_template("site/products.html")
