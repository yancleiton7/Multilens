from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from multilens.ext.db.models import Doctor, Institution, Order, Storage

from .form import FormDoctor, FormInstitution, FormOrder

bp = Blueprint("site", __name__)


@bp.route("/", methods=["GET"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

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
        return render_template("forms/doctor.html", form=form)

    elif request.method == "POST":
        if form.validate_on_submit():
            response = Doctor.create_by_form(form)

            if response["success"]:
                flash(
                    response["message"],
                    "is-success",
                )

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

        return render_template("forms/doctor.html", form=form)


@bp.route("/medicos/<int:register>", methods=["GET", "POST"])
@login_required
def doctor(register: int):
    doctor_data = Doctor.query.get_or_404(register)
    form = FormDoctor()

    if request.method == "GET":
        if doctor_data is None:
            flash("Cadastro não localizado!", "is-warning")
            redirect(url_for("site.form_doctor"))

        else:
            form.load(doctor_data)

    elif request.method == "POST":
        if form.validate_on_submit():
            response = doctor_data.update_by_form(form)

            if response["success"]:
                flash(response["message"], "is-success")

            else:
                flash(response["message"], "is-danger")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    return render_template("forms/doctor.html", form=form)


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
            response = Institution.create_by_form(form)

            if response["success"]:
                flash(response["message"], "is-success")

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
    institution_data = Institution.query.get_or_404(register)

    if request.method == "GET":
        form.load(institution_data)

    elif request.method == "POST":
        if form.validate_on_submit():
            response = institution_data.update_by_form(form)

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
    return render_template(
        "site/storage.html", products=Storage.query.filter_by(avaliable=True).all()
    )


@bp.route("/vendas/", methods=["GET"])
@login_required
def sales():
    return render_template("site/sales.html")


@bp.route("/vendas/nova", methods=["GET", "POST", "DELETE"])
@login_required
def register_sale():
    status = 200
    form = FormOrder()
    user_order = Order.get_current_user_order()

    if request.method == "GET":
        pass

    elif request.method == "POST":
        if form.validate_on_submit():
            response = user_order.add_item_by_form(form)
            if not response["success"]:
                flash(response["message"], "is-warning")

        else:
            for field in form.errors.values():
                [flash(err, "is-danger") for err in field]

    elif request.method == "DELETE":
        item_id = request.args.get("item_id")
        if item_id is not None:
            user_order.remove_item(item_id)

            response = {
                "success": True,
                "message": "Item excluido com sucesso!",
            }

        else:
            response = {
                "success": False,
                "message": "Não foi possível processar sua solicitação, verifique os parâmetros informados",
            }

        return response

    return (
        render_template("forms/sale.html", form=form, order=user_order.get_details()),
        status,
    )


@bp.route("/vendas/finalizar", methods=["GET", "POST"])
@login_required
def finish_sale():
    return render_template("site/finish_order.html")
