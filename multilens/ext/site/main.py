from urllib.parse import urljoin, urlparse

from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user

from multilens.ext.auth import validate_user
from multilens.ext.db.models import Doctor, Institution, Register

from .form import FormDoctor, FormInstitution, FormLogin

from sqlalchemy.exc import IntegrityError

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

        if response["success"]:
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
            register = Register()

            form.populate_obj(register)
            register.type = "doctor"
            register.save()

            form.populate_obj(doctor)
            doctor.register_id = register.id
            response = doctor.save()

            if response["success"]:
                flash(response["message"], "is-success",)

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

        return render_template("forms/doctors.html", form=form)


@bp.route("/medicos/<int:register>", methods=["GET", "POST"])
@login_required
def doctor(register: int):
    doctor_data = Doctor.query.outerjoin(
        Register, Doctor.register_id == Register.id
    ).filter(Doctor.id == register).first()
    form = FormDoctor(obj=doctor_data)

    if request.method == "GET":
        if doctor_data is None:
            flash("Cadastro não localizado!", "is-warning")
            redirect(url_for("site.form_doctor"))

        else:
            form.speciality_id.data = doctor_data.speciality
            form.zip.data = doctor_data.register.zip
            form.address.data = doctor_data.register.address
            form.country.data = doctor_data.register.country
            form.district.data = doctor_data.register.district

    elif request.method == "POST":
        if form.validate_on_submit():
            register_data = Register.query.filter_by(id=doctor_data.register_id).first()
            form.populate_obj(doctor_data)
            form.populate_obj(register_data)

            register_data.save()
            response = doctor_data.save()

            if response["success"]:
                flash(response["message"], "is-success")

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    return render_template("forms/doctors.html", form=form)


@bp.route("/instituicoes/", methods=["GET"])
@login_required
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
            register = Register()
            institution = Institution()

            form.populate_obj(register)
            register.type = "institution"
            register.save()

            form.populate_obj(institution)
            institution.register_id = register.id
            response = institution.save()

            if response["success"]:
                flash(response["message"] + f"{register.id}", "is-success")

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    return render_template("forms/institution.html", form=form)


@bp.route("/instituicoes/<int:register>", methods=["GET", "POST"])
@login_required
def institution(register: int):
    form = FormInstitution()
    institution_data = Institution.query.outerjoin(
        Register, Institution.register_id == Register.id
    ).filter(Institution.id == register).first()

    if request.method == "GET":
        if institution_data is None:
            flash("Cadastro não localizado!", "is-warning")
            redirect(url_for("site.form_institution"))

        else:
            form.process(obj=institution_data)
            form.zip.data = institution_data.register.zip
            form.address.data = institution_data.register.address
            form.country.data = institution_data.register.country
            form.district.data = institution_data.register.district

    elif request.method == "POST":
        if form.validate_on_submit():
            register_data = Register.query.filter_by(id=institution_data.register_id).first()
            form.populate_obj(institution_data)
            form.populate_obj(register_data)
            register_data.save()
            response = institution_data.save()

            if response["success"]:
                flash(response["message"], "is-success")

            else:
                flash(response["message"], "is-danger")

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
